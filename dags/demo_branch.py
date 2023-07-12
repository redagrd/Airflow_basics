# import des librairies
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from datetime  import datetime

# definition de mon dag
@dag(
    dag_id="demo_branch_simple",
    start_date=datetime(2023, 7, 12),
    catchup=False,
)
def simpleBranch():
    # creation de taches multiples
    t0 = EmptyOperator(task_id="t0")
    t1 = EmptyOperator(task_id="t1")
    t2 = EmptyOperator(task_id="t2")
    t3 = EmptyOperator(task_id="t3")
    t4 = EmptyOperator(task_id="t4")
    t5 = EmptyOperator(task_id="t5")
    t6 = EmptyOperator(task_id="t6")

    # relation entre les taches
    t0 >> t1
    t1 << t2
    t1 >> [t3, t4]
    t3 >> t5
    t4 >> t6
# appel de mon dag
simpleBranch()