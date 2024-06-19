import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

import scripts.credentials as cr
from scripts.image_load import random_images
from scripts.message_send_requests import send_message_requests
from scripts.quote_and_image_compiler import put_quote_on_image
from scripts.quote_load import get_quote


with DAG(
        dag_id="MSI_6_dag",
        start_date=pendulum.today(),
        schedule_interval='0 12 * * 0-2,4-6',
        tags=["MSI6"],
        catchup=False,
) as dag:
    start_op = EmptyOperator(task_id="start")

    get_quote_op = PythonOperator(
        task_id='get_quote',
        python_callable=get_quote,
        provide_context=True,
    )

    get_image_op = PythonOperator(
        task_id='get_image',
        python_callable=random_images,
        provide_context=True,
        op_kwargs={"pexel_api_key": cr.PEXEL_API_KEY},
    )

    put_quote_on_image_op = PythonOperator(
        task_id='put_quote_on_image_teams',
        python_callable=put_quote_on_image,
        provide_context=True,
    )

    send_message_op = PythonOperator(
        task_id='send_message',
        python_callable=send_message_requests,
        provide_context=True,
        op_kwargs={
            "webhook_url": cr.WEBHOOK_TEAMS,
            "message_sender_name": cr.MESSAGE_SENDER_NAME,
        },
    )

    finish_op = EmptyOperator(task_id="finish")

    start_op >> [get_quote_op, get_image_op] >> put_quote_on_image_op >> send_message_op >> finish_op
