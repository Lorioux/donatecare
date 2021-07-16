setup:
	# Preparing virtual environment to installing core dependencies
	python -m venv .venv

install:
	# Updating package installer
	# Installing dependecies
	python -m pip install --upgrade pip &&\
	pip install -r requirements.txt &&\
	
lint:
	# Scanning dockerfile
	hadolint --ignore DL3003 ./Dockerfile
	# Scanning source code
	pylint --ignore=migrations -d W app.py registration/microservice.py

test:
	pytest --verbose --junit-logging system-out


all: install lint test