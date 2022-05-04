from datetime import datetime
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.models import Variable

USERNAME = Variable.get("USERNAME")
PASSWORD = Variable.get("PASSWORD")

default_args = {
    'owner'      : 'airflow',
    'description': 'Make RU Meal Reservation',
    'start_date' : datetime(2022, 5, 1),
    'retries'    : 0
}

def build_reservation_task(target_meal):
    meal = {
        'lunch': 'Almoço',
        'dinner': 'Jantar'
    }

    return DockerOperator(
        task_id=f'make_reservation_{target_meal}',
        image='ru-crawler',
        auto_remove=True,
        docker_url="TCP://docker-socket-proxy:2375",
        network_mode="bridge",
        environment={
            'MEAL': meal.get(target_meal),
            'PASS': PASSWORD,
            'USER': USERNAME
        }
    )

with DAG(
    'ru_meal_reservation',
    default_args=default_args,
    schedule_interval="0 15 * * *",
    catchup=False
) as dag:

    make_lunch_reservation = build_reservation_task('lunch')
    make_dinner_reservation = build_reservation_task('dinner')

    make_lunch_reservation >> make_dinner_reservation
