import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

import scripts.credentials as cr
import scripts.main as m


with DAG(
        dag_id="MSI_4_dag",
        start_date=pendulum.today(),
        schedule_interval='0 12 * * 3',
        tags=["MSI4"]
) as dag:
    start_op = EmptyOperator(task_id="start")

    send_quote_teams_op = PythonOperator(
        task_id='send_quote_with_toads_to_teams',
        python_callable=m.main_msi_4,
        op_kwargs={"pexel_api_key": cr.PEXEL_API_KEY,
                   "webhook_teams": cr.WEBHOOK_TEAMS,
                   "message_sender_name": cr.MESSAGE_SENDER_NAME},
    )

    finish_op = EmptyOperator(task_id="finish")

    start_op >> send_quote_teams_op >> finish_op