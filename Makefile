build:
	docker build -t naturalett/playground:latest .
tag:
	docker tag naturalett/playground:latest naturalett/playground:v1
push:
	docker push naturalett/playground:latest
	docker push naturalett/playground:v1
