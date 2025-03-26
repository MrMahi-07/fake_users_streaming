from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import today
from kafka_scripts.kafka_user_consumer import consume_messages

# Default arguments for DAG
default_args = {
    "owner": "airflow",
    "start_date": today("UTC").add(days=-1),
    "retries": 1,
}

with DAG(
    dag_id="kafka_consumer_dag",
    default_args=default_args,
    schedule_interval=None,  # manually trigger from UI
    catchup=False,
    tags=["kafka"],
) as dag:

    PythonOperator(
        task_id="run_kafka_consumer",
        python_callable=consume_messages,
        op_args=[3],
    )
