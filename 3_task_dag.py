import pendulum
from airflow import DAG
from airflow.models.baseoperator import chain_linear
from airflow.operators.empty import EmptyOperator

with DAG(
        dag_id="3_task_dag",
        start_date=pendulum.today(),
        schedule_interval=None,
        tags=["30_2_hw"],
        catchup=False,
) as dag:
    start_1_op = EmptyOperator(task_id="start_1")
    start_2_op = EmptyOperator(task_id="start_2")
    start_3_op = EmptyOperator(task_id="start_3")

    do_smth_1_op = EmptyOperator(task_id="do_smth_1")
    do_smth_2_op = EmptyOperator(task_id="do_smth_2")
    do_smth_3_op = EmptyOperator(task_id="do_smth_3")

    finish_1_op = EmptyOperator(task_id="finish_1")
    finish_2_op = EmptyOperator(task_id="finish_2")

    chain_linear(
        [start_1_op, start_2_op, start_3_op],
        [do_smth_1_op, do_smth_2_op, do_smth_3_op],
        [finish_1_op, finish_2_op]
    )

