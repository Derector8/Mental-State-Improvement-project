# Mental-State-Improvement-project
A service which would send to users a beautiful image with an inspiring quote on it (or toads on wednesdays) on a daily routine, except restricted dates.

#### Project contains 2 folders:
  * airflow - main project folder.  
    
  * script_without_orchestration - folder with additional scripts from 1 sprint to send a quote with image manually, without using airflow.  


  ## Description:
#### airflow project contains: 
    1) Dockerfile and docker-compose.yml files of apache-airflow 2.8.1 (with postgres) for Docker's automated build
    2) requirements.txt with project dependencies
    3) config/airflow.cfg for editing airflow configuration
    4) dags folder for dags
    5) dags/scripts for project functions 
    
  ## Installation
  #### Note: Don't forget to install Docker and Docker-compose.
  1) Download this repo.
  2) To run the app open .../Mental-State-Improvement-project/airflow/ and use command:

     ```bash
     docker-compose up
     ```
  3) Fill in your credentials (Pexel API key and MS Teams Webhook url) in /Mental-State-Improvement-project/airflow/dags/scripts/credentials.py  
     or instead  
     For more safe usage of your credentials you can open main_dag.py(/Mental-State-Improvement-project/airflow/dags/main_dag.py) in editor, comment this 2 lines(below the imports):
     
     ```python
     Variable.set(key="secret_pexel_api_key", value=f"{cr.PEXEL_API_KEY}")
     Variable.set(key="secret_teams_webhook_url", value=f"{cr.WEBHOOK_TEAMS}")
     ```
     And set variables(secret_pexel_api_key, secret_teams_webhook_url) manually in airflow UI.
     
  5) Visit Airflow UI (default: http://localhost:8080/) and trigger MSI_main_dag.

  ## FAQ:
  * To send an inspiring quote with image manually:  
        1) Open script_without_orchestration folder  
        2) Fill in your credentials(your name, pexel API key and teams webhook url) in credentials.py  
        3) Run main.py
