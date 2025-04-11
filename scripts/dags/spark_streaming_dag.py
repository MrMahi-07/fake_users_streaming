from airflow import DAG
from airflow.operators.bash import BashOperator
from pendulum import today

default_args = {
    "owner": "airflow",
    "start_date": today("UTC").add(days=-1),
    "email_on_failure": False,
    "retries": 0,
}

with DAG(
    dag_id="spark_job_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="A DAG to run Spark job using BashOperator",
    tags=["spark", "job"],
) as dag:

    run_spark_job = BashOperator(
        task_id="run_spark_job",
        bash_command="docker exec spark-master spark-submit /opt/spark/app/spark_streaming.py",
    )
