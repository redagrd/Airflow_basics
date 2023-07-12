# import des librairies
from airflow import DAG
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from datetime  import datetime
from random import randint

# arguments par defaut
defaut_args = {
    "start_date": datetime(2023, 7, 12),
    "retries": 1
}

# ma fonction aux choix multiples
def _mon_eval_model():
    accuracy = randint(0, 100)
    print(f"accuracy: {accuracy}")
    if accuracy > 70:
        return ["super_accurate", "accurate"]
    elif accuracy > 50:
        return "accurate"
    return "not_accurate"

# declaration de mon dag par contexte
with DAG(
    dag_id="demo_branch_optionnel",
    schedule="@once",
    catchup=False,
    default_args=defaut_args
) as dag:
    # tache 1 simuler la création du model
    t1 = DummyOperator(
        task_id="create_model"
    )
    # tache 2 branchement sur son evaluation
    choose_best = BranchPythonOperator(
        task_id="choose_best",
        python_callable=_mon_eval_model
    )
    # tacche 3 du choix "super_accurate"
    super_accurate = DummyOperator(
        task_id="super_accurate"
    )
    # tache 4 du choix "accurate"
    accurate = DummyOperator(
        task_id="accurate"
    )
    # tache 5 du choix "not_accurate"
    not_accurate = DummyOperator(
        task_id="not_accurate"
    )

    # relation entre les taches
    t1 >> choose_best >> [super_accurate, accurate, not_accurate]