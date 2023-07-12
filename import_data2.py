from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
import requests
import json
import pandas as pd

# definition de mon dag
@dag(
    dag_id = "AAAA",
    schedule_interval="@once",
    start_date = datetime(2023,7,11),
    catchup = False,
    dagrun_timeout = timedelta(minutes=10),
)
def extract_to_postgres():
    # Tache 1 Create table if not exist
    create_drivers_table = PostgresOperator(
        task_id="create_drivers_table",
        postgres_conn_id="tutorial_pg_conn",
        sql="sql/drivers_table.sql"
    )
    # Tache 2 recuperation des data via une API
    @task(task_id="get_data_to_local")
    def get_data_to_local():
        # URL de ma requete API
        url = "https://data.cityofnewyork.us/resource/4tqt-y424.json"
        response = requests.get(url)
        
        # Récuperation des données du "content" en json
        data_json = json.loads(response.content)
        # Utilisation de pandas pour charger mes datas en CSV
        df = pd.DataFrame(data_json)
        df.to_csv("/opt/airflow/dags/file/drivers.csv",
                sep=";",
                escapechar="\\",
                encoding='utf-8',
                quoting=1
        )
    #  Relation entre mes taches
    create_drivers_table >> get_data_to_local()

extract_to_postgres()