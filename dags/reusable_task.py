# import des librairies
from airflow.decorators import dag, task
from datetime import datetime

# Creation d'une tache reutilisable
@task
def addition(x,y):
    print(f"addition de x={x} et y={y}")
    return x+y



# declaration de mon dag
@dag(
    dag_id="reusable_task",
    start_date=datetime(2023, 7, 13),
    
)
def reusable_dag():
    # appel d'une tache
    debut = addition.override(task_id="debut")(1,2)
    # reutilisation multiple
    for i in range(10):
        debut >> addition.override(task_id=f"suite_{i}")(debut, i)


# appel de mon dag
reusable_dag()