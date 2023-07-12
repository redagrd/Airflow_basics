# Airflow


## Bases

DAG = Directed Acyclic Graph
constitué de tâches (tasks) et d'opérateurs (operators), c'est l'équivalent d'un script python

Paramètres d'une tâche:
dag_id: identifiant du flux de travail
start_date: date de début du flux de travail
schedule_interval: fréquence d'exécution du flux de travail
catchup: relance l'execution si echec
dagrun_timeout: la durée maximale d'exécution du flux de travail

Scheduler:

- lit les DAGs
- planifie les tâches
- les exécute
- gère les dépendances entre les tâches
- gère les erreurs

Executor:

- exécute les tâches
- gère les erreurs

## Deployer Airflow avec docker:

```powershell
curl -O docker-compose.yaml
Uri: https://airflow.apache.org/docs/apache-airflow/2.6.2/docker-compose.yaml
```

ajout d'un adminer dans les services du docker-compose.yaml

```yaml	
adminer:
    image: adminer
    restart: always
    ports:
      - 7080:8080
    depends_on:
      - postgres
```

initialisation du docker-compose. Permet de créer les images et les containers. Nécessaire uniquement lors du premier lancement. On ne peut pas lancer le docker-compose up sans avoir fait l'initialisation.

```powershell
docker-compose up airflow-init
```

lancement du docker-compose

```powershell
docker-compose  up
```

## Script DAG

Un script DAG n'est pas un script python classique. Il est exécuté par l'airflow scheduler.  
Il y a plusieurs façons de créer un DAG:

- Declaration par le contexte

```python
import datetime
# import des librairies airflow
from airflow import DAG
from airflow.operators.empty import EmptyOperator
with DAG(
  dag_id="declaration_contexte",
  start_date = datetime.datetime(2021, 1, 1),
  schedule="@daily",
  default_args={​"key":"value"}​
):
  # contexte d'execution de mes taches
  EmptyOperator(task_id="task")
```

- Declaration par constructeur

```python
import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
# declaration par constructeur
my_dag = DAG(
    dag_id="declaration_constructeur",
    start_date=datetime.datetime(2021, 1, 1),
    schedule="@daily",
)
# appel d'execution d'une tache dans mon DAG
EmptyOperator(task_id="task", dag=my_dag)
```

- Declaration par annotation

```python
# import des librairies
import datetime
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
# declaration par annotation
@dag(
    dag_id="declaration_annotation",
    start_date=datetime.datetime(2021, 1, 1),
    schedule="@daily")
def generate_dag():
    # appel d'execution d'une tache dans mon DAG
    EmptyOperator(task_id="task")
# execution du DAG
generate_dag()
```

## Operateurs

### BaseOperator

BaseOperator est la classe de base de tous les opérateurs. Elle permet de définir les paramètres de base d'une tâche.

- Operators

Les operators sont ce qui va executer l'opérations des tâches du DAG. Il existe plusieurs types d'operators.

- Sensors

Une sous classe d'operator spécifique sensible à un environnement extérieur.

- @task

Une anotation de fonction pour signaler une tâche en python.

### Operateurs de gestion

- DummyOperator
Créer une tâche fictive. Permet de créer des dépendances entre les tâches sans effectuer d'action concrète.

- BranchPythonOperator
Effectue une branche conditionnelle basée sur le résultat d'une fonction python.

- SensorOperator
Effectue une attente jusqu'à ce qu'un critère soit rempli. Il est utilisé pour surveiller les changements d'état avant de déclencher une autre tâche.

