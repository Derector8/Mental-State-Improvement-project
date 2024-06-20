from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import (
    PythonOperator,
    BranchPythonOperator,
)
from airflow.utils.trigger_rule import TriggerRule

import scripts.credentials as cr
from scripts.image_load import (
    random_images,
    search_images,
)
from scripts.send_message import send_message
from scripts.quote_and_image_compiler import prepare_image
from scripts.quote_load import (
    get_quote,
    get_quote_toads,
)
from scripts.additional_functions import (
    check_wednesday,
    check_restricted_dates,
)


with DAG(
        dag_id="MSI_main_dag",
        start_date=datetime(2024, 6, 20),
        schedule_interval="0 12 * * *",
        tags=["MSI_final", "main"],
        catchup=False,
) as dag:
    start_op = EmptyOperator(task_id="start")

    check_restricted_dates_op = BranchPythonOperator(
        task_id="check_restricted_dates",
        python_callable=check_restricted_dates,
        provide_context=True,
    )

    check_wednesday_op = BranchPythonOperator(
        task_id="check_wednesday",
        python_callable=check_wednesday,
        provide_context=True,
    )

    get_quote_op = PythonOperator(
        task_id="get_quote",
        python_callable=get_quote,
        provide_context=True,
    )

    get_image_op = PythonOperator(
        task_id="get_image",
        python_callable=random_images,
        provide_context=True,
        op_kwargs={"pexel_api_key": cr.PEXEL_API_KEY},
    )

    get_quote_toads_op = PythonOperator(
        task_id="get_quote_toads",
        python_callable=get_quote_toads,
        provide_context=True,
    )

    get_image_toads_op = PythonOperator(
        task_id="get_image_toads",
        python_callable=search_images,
        provide_context=True,
        op_kwargs={"pexel_api_key": cr.PEXEL_API_KEY},
    )

    put_quote_on_image_op = PythonOperator(
        task_id="put_quote_on_image",
        python_callable=prepare_image,
        provide_context=True,
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    send_message_op = PythonOperator(
        task_id='send_message',
        python_callable=send_message,
        provide_context=True,
        op_kwargs={
            "webhook_url": cr.WEBHOOK_TEAMS,
            "message_sender_name": cr.MESSAGE_SENDER_NAME,
        },
    )

    skip_message_op = EmptyOperator(task_id="skip_message")

    finish_op = EmptyOperator(
        task_id="finish",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    start_op >> check_restricted_dates_op

    check_restricted_dates_op >> skip_message_op >> finish_op
    check_restricted_dates_op >> check_wednesday_op

    check_wednesday_op >> [get_quote_op, get_image_op] >> put_quote_on_image_op
    check_wednesday_op >> [get_quote_toads_op, get_image_toads_op] >> put_quote_on_image_op

    put_quote_on_image_op >> send_message_op >> finish_op
