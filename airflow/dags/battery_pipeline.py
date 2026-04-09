from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import pickle
from sqlalchemy import create_engine

default_args={
    'owner':'avdhi',
    'retries':1,
    'retry_delay':timedelta(minutes=5),
    'start_date':datetime(2025, 1, 1)
}

DB_URL = 'postgresql://avdhipagaria@localhost:5432/battery_health_db'

PROJECT_PATH = '/usr/local/airflow/include'

def load_data():
    print("Loading battery data...")
    df=pd.read_csv(f'{PROJECT_PATH}/merged_df.csv')
    print(f"Loaded {len(df)} rows!")
    return len(df)

def store_to_postgres():
    print("Storing data to PostgreSQL...")
    df=pd.read_csv(f'{PROJECT_PATH}/merged_df.csv')
    engine = create_engine(DB_URL)
    predictions = df[['battery_id', 'cycle_number', 'avg_voltage', 'avg_temperature', 'avg_current', 'SoH', 'RUL']].copy()
    predictions.columns = ['battery_id', 'cycle_number', 'avg_voltage', 'avg_temperature', 'avg_current', 'SoH', 'RUL']
    predictions.to_sql('battery_predictions', engine, if_exists='replace', index=False)

def detect_anomalies():
    print("Detecting anomalies...")
    df=pd.read_csv(f'{PROJECT_PATH}/merged_df.csv')
    with open(f'{PROJECT_PATH}/anomaly_model.pkl', 'rb') as f:
        model_anomaly=pickle.load(f)
    features = df[['avg_voltage', 'avg_temperature', 'avg_current']]
    predictions = model_anomaly.predict(df[features])
    engine = create_engine(DB_URL)
    df['anomaly'] = predictions
    df['anomaly_label'] = df['anomaly'].map({1: 'Normal', -1: 'Anomaly'})
    anomalies = df[df['anomaly_label'] == 'Anomaly']
    [[
        'battery_id', 'cycle_number',
        'avg_voltage', 'avg_temperature',
        'avg_current', 'SoH', 'anomaly_label'
    ]].copy()
    anomalies.to_sql('anomaly_alerts', engine, if_exists='replace', index=False)

with DAG(
    dag_id='battery_health_pipeline',
    default_args=default_args,
    description='End to end battery health ML pipeline',
    schedule='@hourly',
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )

    task2 = PythonOperator(
        task_id='store_to_postgres',
        python_callable=store_to_postgres
    )

    task3 = PythonOperator(
        task_id='detect_anomalies',
        python_callable=detect_anomalies
    )

    # Define order
    task1 >> task2 >> task3