setup: 
	# Preparing virtual environment to installing core dependencies
	python -m venv .venv

install: setup
	# Updating package installer
	# Installing dependecies
	. .venv/bin/activate
	python -m pip install --upgrade pip &&\
	pip install -r requirements.txt
	sudo wget -O hadolint https://github.com/hadolint/hadolint/releases/download/v1.16.3/hadolint-Linux-x86_64
	sudo chmod +x hadolint
	
lint: 
	# Scanning dockerfile
	sudo ./hadolint --ignore DL3003 ./Dockerfile
	# Scanning source code
	. .venv/bin/activate
	black ./
	pylint --ignore=migrations -d W,C0114 app.py \
		registration/microservice.py \
		booking/microservice.py \
		scheduling/microservice.py

migrations: install
	. .venv/bin/activate 
	flask db init --multidb
	flask db stamp head
	flask db migrate
	flask db upgrade

test:
	pytest --verbose --junit-logging system-out


all: install lint test
