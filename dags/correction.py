from datetime import datetime, timedelta
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from random import randint
import os

def nb_random():
    return randint(0, 10000000)

def save_inFile(file, **context):
    with open(file, "a") as f:
        msg = "date : {}, nombre aléatoire : {}"\
            .format(context["execution_date"], nb_random())
        f.write(msg)
        f.write("\n")
@dag(
    dag_id = "exercice_1",
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    start_date=datetime(2023, 7, 1),
    schedule_interval="@daily",
    catchup=True,
)

def mon_dag():
    #chargement du script bash dans lequel le fichier est créé
    t1 = BashOperator(
        task_id="create_file",
        bash_command="/opt/airflow/dags/file/mon_script.sh ", # l'espace est important pour que le script fonctionne, on ne sait pas pourquoi
    )
    t2 = PythonOperator(
        task_id="save_data",
        depends_on_past=False,
        python_callable=save_inFile,
        provide_context=True,
        op_kwargs={"file": "/opt/airflow/dags/file/random_number.txts"},
    )

    t1 >> t2

mon_dag()