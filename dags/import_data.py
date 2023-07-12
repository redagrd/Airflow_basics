# import libraries
from airflow.decorators import dag, task
from datetime  import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
from requests import get
import json
import pandas as pd
import psycopg2 as pg
import os

# definition de mon dag
@dag(
    dag_id="import_data",
    schedule_interval="@once",
    start_date=datetime(2023, 7, 11),
    catchup=False,
    dagrun_timeout=timedelta(minutes=10),
)
def extract_to_postgres():
    # tache 1 create table if not exists
    create_drivers_table = PostgresOperator(
        task_id="create_drivers_table",
        postgres_conn_id="tutorial_pg_conn",
        sql="sql/drivers_table.sql"
    )

    # tache 2  recuperer des données via une api
    @task(task_id="get_data_to_local")
    def get_data_to_local():
        # url de l'api
        url = "https://data.cityofnewyork.us/resource/4tqt-y424.json"
        response = get(url)
        # récupérer mes données du "content" en json
        data_json = json.loads(response.content)
        # utiliser pandas pour charger mes données en csv
        df = pd.DataFrame(data_json)
        df.to_csv("/opt/airflow/dags/file/drivers.csv", sep=";", escapechar="\\", encoding="utf-8", quoting=1)
        
    # tache 3 insertion des données dans ma base de données
    @task(task_id="load_to_postres")
    def load_to_postgres():
        try:
            # ouvrir connexion avec ma base de données
            dbconnect = pg.connect(
                "dbname='airflow' user='airflow' password='airflow' host='postgres'"
            )
            # création d'un curseur pour intéragir avec la bdd
            cursor = dbconnect.cursor()
            with open('/opt/airflow/dags/file/drivers.csv', 'r') as source:
                # skip la ligne de headers
                next(source)
                for row in source:
                    row_split = row.split(";")
                    cursor.execute("""
                        INSERT INTO drivers_data
                        VALUES ('{}', '{}', '{}', '{}', '{}')""".format(
                            row_split[1],
                            row_split[2],
                            row_split[3],
                            row_split[4],
                            row_split[5]
                        )
                    )
                dbconnect.commit()
        except Exception as error:
            print(error)
        finally:
            dbconnect.close()
            
    # tache 4 supprimer les fichiers temporaires
    @task(task_id="delete_temp_files")
    def delete_temp_files():
        try:
            os.remove("/opt/airflow/dags/file/drivers.csv")
        except Exception as error:
            print(error)
    # # autre méthode
    # delete_temp_files() = BashOperator(
    #     task_id="delete_temp_files",
    #     bash_command = "rm /opt/airflow/dags/file/drivers.csv"



# relation entre mes taches
    create_drivers_table >> get_data_to_local() >> load_to_postgres() >> delete_temp_files()

# appel de mon dag
extract_to_postgres()