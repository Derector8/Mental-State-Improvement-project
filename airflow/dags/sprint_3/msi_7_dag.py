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
import scripts.main as m

restricted_dates = [
    datetime(2024, 6, 11).strftime("%Y-%m-%d"),
    datetime(2024, 6, 13).strftime("%Y-%m-%d"),
    datetime(2024, 6, 15).strftime("%Y-%m-%d"),
    datetime(2024, 6, 25).strftime("%Y-%m-%d"),
]


def _skip_messages_on_dates():
    date_now = datetime.today().strftime("%Y-%m-%d")
    if date_now in restricted_dates:
        return "skip_message"
    return "send_quote_on_image_teams"


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

    send_quote_on_image_teams_op = PythonOperator(
        task_id="send_quote_on_image_teams",
        python_callable=m.main_quote_on_image,
        op_kwargs={"pexel_api_key": cr.PEXEL_API_KEY,
                   "webhook_teams": cr.WEBHOOK_TEAMS,
                   "quote_url": cr.QUOTE_URL,
                   "message_sender_name": cr.MESSAGE_SENDER_NAME},
    )

    skip_message_op = EmptyOperator(task_id="skip_message")

    finish_op = EmptyOperator(
        task_id="finish",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    start_op >> check_restricted_dates_op
    check_restricted_dates_op >> send_quote_on_image_teams_op >> finish_op
    check_restricted_dates_op >> skip_message_op >> finish_op
