# créer une tache DAG qui se lance tous les jours, pour créer un nombre aléatoire, et enregister ça à la date du jour dans un fichier texte
# tous les jours a partir du 1er juillet 2023

from datetime import datetime, timedelta
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import random
import os


@dag(
    dag_id = "exo1",
    start_date=datetime(2023, 7, 1),
    schedule_interval="@daily",
    catchup=True,
)
def mon_dag():
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    def generate_random_number():
        return random.randint(0, 10000000)

    def write_random_number():
        path = os.path.join(os.path.dirname(__file__), "random_number.txt") # __file__ = dags\exo1.py ; os.path.dirname(__file__) = dags
        with open(path, "a") as f:
            f.write(str(generate_random_number())+" "+str(datetime.now())+"\n")


    t2 = PythonOperator(
        task_id="generate_random_number",
        python_callable=generate_random_number,
    )

    t3 = PythonOperator(
        task_id="write_random_number",
        python_callable=write_random_number,
    )

    t1 >> t2 >> t3

mon_dag()

#autre solution

# from datetime import datetime, timedelta
# from airflow.decorators import dag
# from airflow.operators.bash import BashOperator
# from airflow.operators.python import PythonOperator
# import random
# import os

# def nb_random():
#     return randint(0, 10000000)
# def save_inFile(file, **context):
#     with open(file, "a") as f:
#         msg = "date : {}, nombre aléatoire : {}"\
#             .format(context["execution_date"], nb_random())
#         f.write(msg)
#         f.write("\n")
# @dag(
#     dag_id = "exercice_1",
#     default_args={
#         "depends_on_past": False,
#         "retries": 1,
#         "retry_delay": timedelta(minutes=5),
#     },
#     start_date=datetime(2023, 7, 1),
#     schedule_interval="@daily",
#     catchup=True,
# )

# def mon_dag():
#     #chargement du script bash dans lequel le fichier est créé
#     t1 = BashOperator(
#         task_id="create_file",
#         bash_command="/opt/airflow/dags/file/mon_script.sh",
#     )
#     t2 = PythonOperator(
#         task_id="save_data",
#         depends_on_past=False,
#         python_callable=save_inFile,
#         provide_context=True,
#         op_kwargs={"file": "/opt/airflow/dags/file/random_number.txt"},
#     )

#     t1 >> t2

# mon_dag()