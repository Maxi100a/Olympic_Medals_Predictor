from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from batch_ingest import download_data
from transform import transform_data
from models import build_models
from analyze import analyze_models

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 12),
    'email': ['aedoesma@vt.edu'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'data_pipeline_dag',
    default_args=default_args,
    description='Execute the data pipeline from downloading data to building machine learning models',
    schedule_interval=timedelta(days=1),
)

ingest_etl = PythonOperator(
    task_id='ingest_dataset',
    python_callable=download_data,
    dag=dag,
)

transform_etl = PythonOperator(
    task_id='transform_dataset',
    python_callable=transform_data,
    dag=dag,
)

model_etl = PythonOperator(
    task_id='build_ML_models',
    python_callable=build_models,
    dag=dag,
)

analyze_etl = PythonOperator(
    task_id='analyze_ML_results',
    python_callable=analyze_models,
    dag=dag,
)

ingest_etl >> transform_etl >> model_etl >> analyze_etl