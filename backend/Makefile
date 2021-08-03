setup: 
	# Preparing virtual environment to installing core dependencies
	python -m venv .venvx

install: setup
	# Updating package installer
	# Installing dependecies
	. .venvx/bin/activate
	python -m pip install --upgrade pip &&\
	pip install -r test-requirements.txt
	# install hadolint in not exists
	if [ -e "./hadolint" ]; then \
		echo "Found hadolint in this directory." ; \
	else \
		sudo wget -O hadolint https://github.com/hadolint/hadolint/releases/download/v1.16.3/hadolint-Linux-x86_64 &&\
		sudo chmod +x hadolint; \
	fi 
	
lint: install
	# Scanning dockerfile
	sudo ./hadolint --ignore DL3003 ./Dockerfile
	# Scanning source code
	black ./
	pylint --ignore=migrations,settings.py,manage.py -d W ./*.py

migrations: 
	flask db init --multidb
	flask db stamp head
	flask db migrate
	flask db upgrade

test:
	pytest --verbose
	rm -f ./hadolint


all: install lint test
