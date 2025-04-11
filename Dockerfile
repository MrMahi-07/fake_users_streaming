FROM apache/airflow:latest

# Set root user
USER root

# upgrade pip
RUN python -m pip install --upgrade pip

# Set root user
USER airflow

COPY /scripts/requirements.txt /opt/airflow/dags/requirements.txt

# Install additional dependencies
RUN pip install --no-cache-dir -r /opt/airflow/dags/requirements.txt