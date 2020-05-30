VER=$(shell git rev-parse --short HEAD)

tag2:
	echo GIT_COMMIT=$(VER)
build:
	docker build -t naturalett/playground:latest -t naturalett/playground:$(VER) .
push:
	docker push naturalett/playground:latest
	docker push naturalett/playground:$(VER)
