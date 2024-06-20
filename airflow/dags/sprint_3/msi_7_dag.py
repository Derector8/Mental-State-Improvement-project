from datetime import datetime

import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import (
    PythonOperator,
    BranchPythonOperator,
)
from airflow.utils.trigger_rule import TriggerRule

import scripts.credentials as cr
from scripts.image_load import random_images
from scripts.message_send_requests import send_message_requests
from scripts.quote_and_image_compiler import put_quote_on_image
from scripts.quote_load import get_quote

restricted_dates = [
    datetime(2024, 6, 11).strftime("%Y-%m-%d"),
    datetime(2024, 6, 13).strftime("%Y-%m-%d"),
    datetime(2024, 6, 15).strftime("%Y-%m-%d"),
    datetime(2024, 6, 25).strftime("%Y-%m-%d"),
]


def _skip_messages_on_dates(**kwargs):
    date_now = kwargs["logical_date"].strftime("%Y-%m-%d")
    if date_now in restricted_dates:
        return "skip_message"
    return ["get_quote", "get_image"]


with DAG(
        dag_id="MSI_7_dag",
        start_date=pendulum.today(),
        schedule_interval="0 12 * * 0-2,4-6",
        tags=["MSI7"],
        catchup=False,
) as dag:
    start_op = EmptyOperator(task_id="start")

    check_restricted_dates_op = BranchPythonOperator(
        task_id="check_restricted_dates",
        python_callable=_skip_messages_on_dates
    )

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

    skip_message_op = EmptyOperator(task_id="skip_message")

    finish_op = EmptyOperator(
        task_id="finish",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    start_op >> check_restricted_dates_op
    check_restricted_dates_op >> [get_quote_op, get_image_op] >> put_quote_on_image_op >> send_message_op >> finish_op
    check_restricted_dates_op >> skip_message_op >> finish_op
