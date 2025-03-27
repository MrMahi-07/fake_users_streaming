from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka_scripts.producer import produce_messages, produce_messages_upto
from pendulum import today

# Default arguments for DAG
default_args = {
    "start_date": today("UTC").add(days=-1),
    "retries": 0,
}

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

# to run the producer for a fixed number of messages
with DAG(
    dag_id="kafka_producer_dag",
    default_args=default_args,
    schedule_interval=None,  # manually trigger from UI
    catchup=False,
    tags=["kafka"],
) as dag:

    PythonOperator(
        task_id="run_kafka_producer",
        python_callable=produce_messages,
        op_args=[10, 3],
    )
