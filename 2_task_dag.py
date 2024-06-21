import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator



with DAG(
        dag_id="2_task_dag",
        start_date=pendulum.today(),
        schedule_interval="0 11-19/2 * * 1-5",
        tags=["30_2_hw"],
        catchup=False,
) as dag:
    start_op = EmptyOperator(task_id="start")

    do_smth_op = EmptyOperator(task_id="do_smth")

    finish_op = EmptyOperator(task_id="finish")

    start_op >> do_smth_op >> finish_op
