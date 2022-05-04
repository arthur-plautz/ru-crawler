
build_image:
	docker build -t ru-crawler .

run_crawler:
	docker run -e MEAL=${MEAL} -e USER=${USER} -e PASS=${PASS} ru-crawler