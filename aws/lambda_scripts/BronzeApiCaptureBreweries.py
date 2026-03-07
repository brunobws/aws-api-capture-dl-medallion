####################################################################
# Author: Bruno William da Silva
# Date: 03/03/2026
#
# Description:
#   Lambda responsible for ingesting brewery data from the
#   Open Brewery DB API into S3 (Bronze layer).
#   Documentantion: https://openbrewerydb.org/documentation
#
# Environment Variables:
#   S3_BUCKET     : (required) Target S3 bucket name
#   ENV           : (required) Execution environment (e.g.: hlg, prd)
#   PER_PAGE      : (optional) Records per page, max 200 (default: 200)
#   TIMEOUT       : (optional) Request timeout in seconds (default: 30)
#   MAX_RETRIES   : (optional) Max retry attempts on failed requests (default: 3)
#   RETRY_BACKOFF : (optional) Exponential backoff multiplier in seconds (default: 2.0)
#  
#   E-mails to alert:
#    You have to 'notification_params' table in Dynamo DB
#
# Trigger:
#   - Airflow Lambda Operator
#   - Manual trigger for testing
####################################################################

######### imports ################
import os
import json
import time
import urllib3
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

# Custom 
from utils import AwsManager,Dynamo
from logs import Logs
from support import split_target_table
#######################################

############### Config globals var ####################################

JOB_NAME      = "BronzeApiCaptureBreweries"
TARGET_TABLE  = "breweries_tb_breweries"

S3_BUCKET     = os.environ["S3_BUCKET"]
ENV           = os.getenv("ENV", "")


BASE_URL      = "https://api.openbrewerydb.org/v1/breweries"
META_URL      = "https://api.openbrewerydb.org/v1/breweries/meta"  # Returns total record count used to calculate number of pages before pagination starts

PER_PAGE      = int(os.getenv("PER_PAGE", 200))                    # Max records per API page (API breweries limit: 200)
TIMEOUT       = int(os.getenv("TIMEOUT", 30))                      # Request timeout in seconds
MAX_RETRIES   = int(os.getenv("MAX_RETRIES", 3))                   # Max retry attempts on failed requests
RETRY_BACKOFF = float(os.getenv("RETRY_BACKOFF", 2.0))             # Exponential backoff multiplier (attempt^n seconds)

#####################################################################



##################### Custom classes and instances #########################


logger = Logs(job_name=JOB_NAME, target_table=TARGET_TABLE, layer="bronze", env=ENV, technology="lambda")

dynamo = Dynamo(job_name=JOB_NAME,
                logger=logger,
                trgt_tbl=TARGET_TABLE)

response = dynamo.get_dynamo_records(dynamo_table='notification_params', 
                                     id_value=TARGET_TABLE, 
                                     id_column='trgt_tbl')

email_on_failure, email_on_warning, email_on_success = dynamo.get_email_notif(response, layer='ingestion')

manager = AwsManager(job_name=JOB_NAME, logger=logger, destination=email_on_failure, target_table=TARGET_TABLE)


is_critical = response.get('critical',False)
logger.add_info(critical=is_critical)


http = urllib3.PoolManager()

########################################################################




####################### API client #################################

def get_json(url: str) -> Any:
    """GET request with exponential-backoff retry."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = http.request("GET", url, timeout=TIMEOUT)

            if response.status == 200:
                return json.loads(response.data.decode("utf-8"))

            wait = RETRY_BACKOFF ** attempt
            print(f"[WARNING] HTTP {response.status} on attempt {attempt}/{MAX_RETRIES}. Retrying in {wait:.1f}s.")
            time.sleep(wait)

        except urllib3.exceptions.HTTPError as e:
            wait = RETRY_BACKOFF ** attempt
            print(f"[WARNING] Connection error on attempt {attempt}/{MAX_RETRIES}: {e}. Retrying in {wait:.1f}s.")
            time.sleep(wait)

    raise RuntimeError(f"All {MAX_RETRIES} attempts failed for: {url}")


def fetch_all_breweries() -> List[Dict[str, Any]]:
    """Fetches all breweries from the API using full paginated snapshot."""


    total   = int(get_json(META_URL).get("total", 0))

    if total == 0:

        logger.warning(warning_mg='empty api response')
        logger.write_log()

        raise ValueError("API returned total=0 from /meta. Aborting ingestion.")
    
    n_pages = -(-total // PER_PAGE)  # ceiling division
    print(f"[INFO] Total records: {total} | Pages to fetch: {n_pages}")

    all_records = []
    for page in range(1, n_pages + 1):
        print(f"[INFO] Fetching page {page}/{n_pages}")
        all_records.extend(get_json(f"{BASE_URL}?page={page}&per_page={PER_PAGE}"))

    print(f"[INFO] Total collected: {len(all_records)} records")
    return all_records


######################## S3 Upload #################################

def upload_to_s3(data: List[Dict[str, Any]]) -> Tuple[str, str]:
    """Serializes records to JSON and uploads to S3 partitioned by ingestion date.
    
    Returns:
        Tuple[str, str]: (ingestion_date, filename)
    """

    now            = datetime.now(tz=timezone.utc)
    ingestion_date = now.strftime('%Y-%m-%d')
    filename       = f"data_{now.strftime('%H%M%S')}.json"
    key            = f"breweries/tb_breweries/ingestion_date={ingestion_date}/{filename}"

    logger.add_info(file_name=filename, count=len(data))

    manager.s3.put_s3_file(
        bucket=S3_BUCKET,
        key=key,
        body=json.dumps(data, indent=2, ensure_ascii=False)
    )

    print(f"[INFO] Uploaded {len(data)} records → s3://{S3_BUCKET}/{key}")

    return ingestion_date, filename

####################################################################


def lambda_handler(event, context):
    print("[INFO] Starting FULL ingestion from Open Brewery DB API")

    try:

        breweries                  = fetch_all_breweries()
        ingestion_date, filename   = upload_to_s3(breweries)

        logger.write_log()

        return {
            "statusCode"     : 200,
            "message"        : "Ingestion completed successfully",
            "total_records"  : len(breweries),
            "ingestion_date" : ingestion_date,
            "filename"       : filename,
        }

    except Exception as e:
        print(f"[ERROR] Lambda execution failed: {e}")
        logger.error(error_msg="Lambda execution failed", error_desc=str(e)) # Custom Log error method to capture exception details

        manager.ses.send_email_on_failure(
            target_table=TARGET_TABLE,
            description=str(e),
            destination=email_on_failure) # Custom SES method to send alert email on failure
                                          

        raise