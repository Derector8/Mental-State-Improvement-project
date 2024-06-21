import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule


def _pick_erp_system():
    #Here some code to choose system(now we want to return always new)
    if True:
        return "fetch_sales_new"
    else:
        return "fetch_sales_old"

with DAG(
    dag_id="4_task_dag",
    start_date=pendulum.today(),
    schedule=None,
    tags=["30_2_hw"]
) as dag:
    start_op = EmptyOperator(task_id="start")

    pick_erp_system_op = BranchPythonOperator(
        task_id="pick_erp_system",
        python_callable=_pick_erp_system
    )

    fetch_sales_new_op = EmptyOperator(task_id="fetch_sales_new")
    fetch_sales_old_op = EmptyOperator(task_id="fetch_sales_old")

    clean_sales_new_op = EmptyOperator(task_id="clean_sales_new")
    clean_sales_old_op = EmptyOperator(task_id="clean_sales_old")

    fetch_weather_op = EmptyOperator(task_id="fetch_weather")
    clean_weather_op = EmptyOperator(task_id="clean_weather")

    join_datasets_op = EmptyOperator(
        task_id="join_datasets",
        trigger_rule=TriggerRule.NONE_FAILED
    )
    train_model_op = EmptyOperator(task_id="train_model")
    deploy_model_op = EmptyOperator(task_id="deploy_model")


    start_op >> pick_erp_system_op
    start_op >> fetch_weather_op >> clean_weather_op

    pick_erp_system_op >> fetch_sales_new_op >> clean_sales_new_op
    pick_erp_system_op >> fetch_sales_old_op >> clean_sales_old_op

    [clean_weather_op, clean_sales_new_op, clean_sales_old_op] >> join_datasets_op
    join_datasets_op >> train_model_op >> deploy_model_op
