from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='kafka_producer_dag',
    default_args=default_args,
    schedule_interval=None,  # manually trigger from UI
    catchup=False,
    tags=['kafka'],
) as dag:

    run_producer = BashOperator(
        task_id='run_kafka_producer',
        bash_command='python /opt/airflow/kafka/kafka_user_producer.py'
    )

with DAG(
    dag_id='test_dag',
    default_args=default_args,
    schedule_interval=None,  # manually trigger from UI
    catchup=False,
    tags=['test'],
) as dag:

    run_consumer = BashOperator(
        task_id='run_helo_world',
        bash_command='echo "Hello, World!"' 
    )