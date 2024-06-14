import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id='load_regions_from_covid_API_dag',
    start_date=pendulum.today(),
    schedule=None,
    tags=['hw 28.1'],
) as dag:
    start_op = EmptyOperator(task_id='start')

    load_covid_regions_op = BashOperator(
        task_id='load_covid_regions',
        bash_command='load_covid_regions.sh',
    )

    finish_op = EmptyOperator(task_id='finish')

    start_op >> load_covid_regions_op >> finish_op
