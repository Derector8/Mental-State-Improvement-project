import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor
from airflow.utils.trigger_rule import TriggerRule


def _success_condition(value):
    return bool(value)


def _failure_condition(value):
    return not bool(value)


with DAG(
        dag_id='sensor_postgres_dag',
        start_date=pendulum.today(),
        schedule=None,
        tags=['hw 28.1']
) as dag:
    start_op = EmptyOperator(task_id='start')

    sql_sensor_op = SqlSensor(
        task_id='check_data_in_contacts_table',
        conn_id="my_postgres",
        sql="SELECT * FROM contacts LIMIT 1",
        success=_success_condition,
        failure=_failure_condition,
        fail_on_empty=True,
        poke_interval=60,
        timeout=60
    )

    finish_success_op = EmptyOperator(task_id='data_appeared_finish')

    finish_failure_op = EmptyOperator(
        task_id='no_data_finish',
        trigger_rule=TriggerRule.ALL_FAILED
    )

    start_op >> sql_sensor_op >> finish_success_op
    start_op >> sql_sensor_op >> finish_failure_op
