from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from kafka_scripts.kafka_user_producer import produce_messages, produce_messages_upto

# Default arguments for DAG
default_args = {
    "start_date": days_ago(1),
    "retries": 1,
}


# to run the producer for a fixed number of messages
with DAG(
    dag_id="kafka_producer_dag",
    default_args=default_args,
    schedule_interval=None,  # manually trigger from UI
    catchup=False,
    tags=["kafka", "fixed"],
) as dag:

    PythonOperator(
        task_id="run_kafka_producer", python_callable=produce_messages, op_args=[10, 3]
    )

# to run the producer for a fixed amount of time
with DAG(
    dag_id="kafka_producer_upto_dag",
    default_args=default_args,
    schedule_interval=None,  # manually trigger from UI
    catchup=False,
    tags=["kafka", "time"],
) as dag:

    PythonOperator(
        task_id="run_kafka_producer_upto",
        python_callable=produce_messages_upto,
        op_args=[30],
    )
