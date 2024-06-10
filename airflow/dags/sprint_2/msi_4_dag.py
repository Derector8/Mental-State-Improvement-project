import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

import sprint_2.scripts.credentials as cr
import sprint_2.scripts.main as m


with DAG(
        dag_id="MSI_2_dag",
        start_date=pendulum.today(),
        schedule_interval='0 12 * * 3',
        tags=["MSI2"]
) as dag:
    start_op = EmptyOperator(task_id="start")

    send_quote_teams_op = PythonOperator(
        task_id='send_quote_with_toads_to_teams',
        python_callable=m.main_msi_4,
        op_kwargs={"pexel_api_key": cr.PEXEL_API_KEY,
                   "webhook_teams": cr.WEBHOOK_TEAMS,
                   "owner": cr.OWNER},
    )

    finish_op = EmptyOperator(task_id="finish")

    start_op >> send_quote_teams_op >> finish_op