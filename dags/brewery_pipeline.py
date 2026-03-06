from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.lambda_function import LambdaInvokeFunctionOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.operators.python import PythonOperator
import json


########## DEFAULT ARGS ##########

default_args = {
    "owner": "bws",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


########## FUNCTION TO PARSE LAMBDA RESPONSE ##########

def parse_lambda_response(ti):
    response = ti.xcom_pull(task_ids="invoke_openbrewery_lambda")

    # Lambda return comes as JSON string
    payload = json.loads(response)

    ingestion_date = payload["ingestion_date"]
    filename = payload["filename"]

    return {
        "ingestion_date": ingestion_date,
        "filename": filename
    }


########## DAG ##########

with DAG(
    dag_id="brewery_pipeline",
    description="Open Brewery API ingestion pipeline",
    default_args=default_args,
    start_date=datetime(2026, 3, 4),
    schedule_interval="0 7 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["lambda", "glue", "medallion"],
) as dag:

    ########## INVOKE LAMBDA ##########

    invoke_lambda = LambdaInvokeFunctionOperator(
        task_id="invoke_openbrewery_lambda",
        function_name="BronzeApiCaptureBreweries",
        invocation_type="RequestResponse",
        log_type="Tail",
        payload=json.dumps(
            {
                "source": "airflow",
                "dag_id": "{{ dag.dag_id }}",
                "execution_date": "{{ ts }}",
                "environment": "prd",
            }
        ),
        aws_conn_id="aws_default",
    )


    ########## PARSE LAMBDA RESPONSE ##########

    parse_lambda = PythonOperator(
        task_id="parse_lambda_response",
        python_callable=parse_lambda_response,
    )


    ########## BRONZE TO SILVER ##########

    bronze_to_silver = GlueJobOperator(
        task_id="bronze_to_silver",
        job_name="bronze_to_silver",
        script_args={
            "--dt_ref": "{{ ti.xcom_pull(task_ids='parse_lambda_response')['ingestion_date'] }}",
            "--file_name": "{{ ti.xcom_pull(task_ids='parse_lambda_response')['filename'] }}",
            "--target_table": "breweries_tb_breweries",
        },
        aws_conn_id="aws_default",
        wait_for_completion=True,
    )


    ########## SILVER TO GOLD ##########

    silver_to_gold = GlueJobOperator(
        task_id="silver_to_gold",
        job_name="silver_to_gold",
        script_args={
            "--target_table": "breweries_tb_ft_breweries_agg",
        },
        aws_conn_id="aws_default",
        wait_for_completion=True,
    )


    ########## PIPELINE ORDER ##########

    invoke_lambda >> parse_lambda >> bronze_to_silver >> silver_to_gold
