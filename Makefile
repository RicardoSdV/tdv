.ONESHELL:
SHELL := /bin/bash

DB_USER := $(USER)
DB_NAME := 'tdvdb'
DB_PASSWORD := 'password'
DB_HOST := 'localhost'
ALEMBIC_INI_PATH := $(CURDIR)/tdv/storage/alembic/alembic.ini



.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: req
req:  # Install all packages listed in requirements.txt
	pip install -r requirements.txt

.PHONY: setup
setup:  # Build the project to be able to run the CLI
	pip install -e .

.PHONY: sys_vars
sys_vars:  # Set system variables
	export PYTHONPATH=$(CURDIR)
	export TDV_DB_USER=$(DB_USER)
	export TDV_DB_NAME=$(DB_NAME)
	export TDV_DB_PASSWORD=$(DB_PASSWORD)
	export TDV_DB_HOST=$(DB_HOST)
	export ALEMBIC_CONFIG=$(ALEMBIC_INI_PATH)

.PHONY: postgresql
postgresql:  # Download PostgreSQL (Only valid for Ubuntu)
	sudo apt update
	sudo apt install postgresql postgresql-contrib

.PHONY: create_db_user
create_db_user:
	sudo -u postgres psql -c "CREATE USER $(DB_USER) WITH PASSWORD $(DB_PASSWORD);"

.PHONY: create_db
create_db:
	sudo -u postgres psql -c "CREATE DATABASE $(DB_NAME) OWNER $(DB_USER);"

.PHONY: drop_db
drop_db:
	sudo -u postgres psql -c "DROP DATABASE $(DB_NAME);"

.PHONY: upgrade
upgrade:
	alembic upgrade head

.PHONY: downgrade_all
downgrade_all:
	alembic downgrade base

