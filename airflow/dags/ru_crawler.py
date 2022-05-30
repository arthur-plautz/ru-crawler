from datetime import datetime
import base64
import json
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.models import Variable

USERS = Variable.get("users")

default_args = {
    'owner'      : 'airflow',
    'description': 'Make RU Meal Reservation',
    'start_date' : datetime(2022, 5, 27),
    'retries'    : 1
}

def users_list():
    users_json = base64.b64decode(USERS).decode('ascii').replace("'", '"')
    return json.loads(users_json)

def build_reservation_task(target_meal, email, name, password):
    meal = {
        'lunch': 'Almoço',
        'dinner': 'Jantar'
    }

    return DockerOperator(
        task_id=f'make_{target_meal}_reservation_for_{name}',
        image='ru-crawler',
        auto_remove=True,
        docker_url="TCP://ru-docker-socket-proxy:2375",
        network_mode="bridge",
        environment={
            'MEAL': meal.get(target_meal),
            'PASS': password,
            'USER': email
        }
    )

with DAG(
    'ru_meal_reservation',
    default_args=default_args,
    schedule_interval="0 6 * * *",
    catchup=True
) as dag:

    for user in users_list():
        make_lunch_reservation = build_reservation_task('lunch', **user)
        make_dinner_reservation = build_reservation_task('dinner', **user)

        make_lunch_reservation >> make_dinner_reservation
