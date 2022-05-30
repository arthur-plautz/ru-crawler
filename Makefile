
build_image:
	docker build -t ru-crawler .

run_crawler:
	docker run -e MEAL=${MEAL} -e USER=${USER} -e PASS=${PASS} ru-crawler

run_airflow:
	cd airflow && docker-compose up -d

stop_airflow:
	cd airflow && docker-compose down

update_credentials:
	docker exec airflow-webserver-ru-crawler airflow variables set 'users' ${CREDENTIALS}