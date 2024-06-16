import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

import scripts.credentials as cr
import scripts.main as m


with DAG(
        dag_id="MSI_6_dag",
        start_date=pendulum.today(),
        schedule_interval='0 12 * * 0-2,4-6',
        tags=["MSI6"]
) as dag:
    start_op = EmptyOperator(task_id="start")

    send_quote_teams_op = PythonOperator(
        task_id='send_quote_on_image_teams',
        python_callable=m.main_quote_on_image,
        op_kwargs={"pexel_api_key": cr.PEXEL_API_KEY,
                   "webhook_teams": cr.WEBHOOK_TEAMS,
                   "quote_url": cr.QUOTE_URL,
                   "message_sender_name": cr.MESSAGE_SENDER_NAME},
    )

    finish_op = EmptyOperator(task_id="finish")

    start_op >> send_quote_teams_op >> finish_op
