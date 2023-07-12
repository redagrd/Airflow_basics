# importation des librairies
from airflow import DAG
from datetime import datetime
from airflow.sensors.filesystem import FileSensor
from airflow.exceptions import AirflowSensorTimeout
from airflow.operators.python import PythonOperator

# methode pour vérifier si on sensor à échoué
def _failure_callback(context):
    if isinstance(context["exception"], AirflowSensorTimeout):
        print(context)
        print("sensor timeout")

# fausse fonctions
def _process():
    pass

def _store():
    pass

# declaration de mon dag par contexte
with DAG(
    dag_id="demo_sensor",
    schedule_interval="@daily",
    catchup=False,
    start_date=datetime(2023, 7, 13)
) as dag:
    # taches multiples
    check_partners = [ FileSensor(
        task_id=f'sensor_{partner}',
        poke_interval=120,
        timeout=60 * 30, # 30 minutes timeout
        mode="reschedule", # poke mode is the default mode, you can use it for your use case. reschedule mode is also available and can be used for example if you want to check a file every 5 minutes and reschedule the task if the file is not present.
        filepath=f'$AIRFLOW_HOME/dags/file/partner_{partner}.txt',
        on_failure_callback=_failure_callback,
        fs_conn_id=''
        ) for partner in ["Jean", "Paul", "Jacques"]]

    # tache 2
    process = PythonOperator(
        task_id="process_data",
        python_callable=_process
    )
    # tache 3
    stockage_data = PythonOperator(
        task_id="stockage_data",
        python_callable=_store
    )

# appel des taches
check_partners >> process >> stockage_data