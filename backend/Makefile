setup:
	# Preparing virtual environment to installing core dependencies
	python -m venv .venv

install:
	# Updating package installer
	# Installing dependecies
	# . .venv/bin/activate
	python -m pip install --upgrade pip &&\
	pip install -r requirements.txt
	
lint:
	# Scanning dockerfile
	hadolint --ignore DL3003 ./Dockerfile
	# Scanning source code
	pylint --ignore=migrations -d W,C0114 app.py \
		registration/microservice.py \
		booking/microservice.py \
		scheduling/microservice.py

migrations: 
	. .venv/bin/activate 
	flask db init --multidb
	flask db stamp head
	flask db migrate
	flask db upgrade

test:
	pytest --verbose --junit-logging system-out


all: install lint test