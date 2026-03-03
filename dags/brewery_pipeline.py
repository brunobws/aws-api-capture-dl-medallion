from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.lambda_function import LambdaInvokeFunctionOperator
import json


# =====================================================
# DEFAULT ARGS
# =====================================================

default_args = {
    "owner": "bruno",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


# =====================================================
# DAG
# =====================================================

with DAG(dag_id="brewery_pipeline", description="DAG para ingestão FULL da Open Brewery API para Bronze Layer",default_args=default_args,start_date=datetime(2026, 3, 1),schedule_interval="@daily",catchup=False,max_active_runs=1,tags=["bronze", "lambda", "openbrewery"]) as dag:

    invoke_lambda = LambdaInvokeFunctionOperator(
        task_id="invoke_openbrewery_lambda",
        function_name="BronzeApiCaptureBreweries",  
        invocation_type="RequestResponse",  
        log_type="Tail",
        payload=json.dumps({
                "source": "airflow",
                "dag_id": "{{ dag.dag_id }}",
                "execution_date": "{{ ts }}",
                "environment": "prd"
            }),
        aws_conn_id="aws_default"
    )

    invoke_lambda