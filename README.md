# Mental-State-Improvement-project
A service which would send to users a beautiful image with an inspiring quote on a daily routine.

Sprint 1:
Script for loading images and quotes from API's and sending them in MS Teams channel.

Sprint 2:
added docker-compose to launch locally own airflow server. All script's custom imports changed according to airflow container structure.
Added msi_2_dag with schedule to send quotes daily, except wednesday.
Added msi_4_dag with schedule to send quotes with toads only on wednesdays.
