from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime

default_args = {
    "start_date": days_ago(1),
    'retries': 1,
}

with DAG(
    dag_id='kafka_consumer_dag',
    default_args=default_args,
    schedule_interval=None,  # manually trigger from UI
    catchup=False,
    tags=['kafka'],
) as dag:

    run_consumer = BashOperator(
        task_id='run_kafka_consumer',
        bash_command='python /opt/airflow/kafka/kafka_user_consumer.py'
    )
