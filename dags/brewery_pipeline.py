from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.lambda_function import LambdaInvokeFunctionOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
import json


########## DEFAULT ARGS ##########

default_args = {
    "owner": "bws",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
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

    ########## TASK 1 - INVOKE LAMBDA ##########

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

    ########## TASK 2 - BRONZE TO SILVER ##########

    bronze_to_silver = GlueJobOperator(
        task_id="bronze_to_silver",
        job_name="bronze_to_silver",
        script_args={
            "--dt_ref": "{{ ti.xcom_pull(task_ids='invoke_openbrewery_lambda')['ingestion_date'] }}",
            "--file_name": "{{ ti.xcom_pull(task_ids='invoke_openbrewery_lambda')['filename'] }}",
            "--target_table": "breweries_tb_breweries",
        },
        aws_conn_id="aws_default",
        wait_for_completion=True,
    )

    ########## TASK 3 - SILVER TO GOLD ##########

    silver_to_gold = GlueJobOperator(
        task_id="silver_to_gold",
        job_name="silver_to_gold",
        script_args={
            "--target_table": "breweries_tb_breweries",
        },
        aws_conn_id="aws_default",
        wait_for_completion=True,
    )

    ########## PIPELINE ORDER ##########

    invoke_lambda >> bronze_to_silver >> silver_to_gold