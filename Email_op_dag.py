import pendulum
from airflow.models import DAG
from airflow.operators.email import EmailOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id='email_send_dag',
    start_date=pendulum.today(),
    schedule=None,
    tags=['hw 28.1'],
) as dag:
    start_op = EmptyOperator(
        task_id="start"
    )

    email_op = EmailOperator(
        task_id="email yourself",
        to="bucharevroman@gmail.com",
        subject='Message from Airflow',
        html_content='<p>Hello from Airflow</p>',
        conn_id='my_gmail_conn',
    )

    finish_op = EmptyOperator(
        task_id="finish"
    )

    start_op >> email_op >> finish_op
