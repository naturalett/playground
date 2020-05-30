VER=$(shell git rev-parse --short HEAD)

tag2:
	echo GIT_COMMIT=$(VER)
build:
	docker build -t naturalett/playground:latest .
tag:
	docker tag naturalett/playground:latest naturalett/playground:$(VER)
push:
	docker push naturalett/playground:latest
	docker push naturalett/playground:$(VER)
