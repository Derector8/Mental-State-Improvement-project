import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor

def _success_condition(value):
    return bool(value)


with DAG(
    dag_id='sensor_postgres_dag',
    start_date=pendulum.today(),
    schedule=None,
    tags=['hw 28.1']
) as dag:
    start_op = EmptyOperator(task_id='start')

    sql_sensor_op = SqlSensor(
        task_id='check_regions_data_in_table',
        conn_id="my_postgres",
        sql="SELECT * FROM regions LIMIT 1",
        success=_success_condition,
        poke_interval=60,
        timeout=60*60
    )

    finish_op = EmptyOperator(task_id='finish')

    start_op >> sql_sensor_op >> finish_op
