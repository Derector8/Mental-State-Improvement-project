import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG(
    dag_id='load_covid_regions_from_to_table_dag',
    start_date=pendulum.today(),
    schedule=None,
    tags=['hw 28.1']
) as dag:
    start_op = EmptyOperator(task_id='start')

    load_data_to_table_op = PostgresOperator(
        task_id='load_covid_regions',
        postgres_conn_id='my_postgres',
        sql="SELECT load_covid_regions_to_table();",
    )

    finish_op = EmptyOperator(task_id='finish')

    start_op >> load_data_to_table_op >> finish_op
