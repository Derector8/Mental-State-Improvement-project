import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator



with DAG(
        dag_id="task_1_dag",
        start_date=pendulum.datetime(2024, 6, 8),
        end_date=pendulum.datetime(2024, 7, 13),
        schedule_interval="@weekly",
        tags=["30_2_hw"],
        catchup=False,
) as dag:
    start_op = EmptyOperator(task_id="start")

    do_smth_op = EmptyOperator(task_id="do_smth")

    finish_op = EmptyOperator(task_id="finish")

    start_op >> do_smth_op >> finish_op
