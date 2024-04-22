
export PYTHONPATH := $(CURDIR)
PRINT_SPACE := @echo ""

DB_USER = $(shell python3 -c 'from tdv.constants import DbInfo; print(DbInfo.USER.value)')
DB_NAME = $(shell python3 -c 'from tdv.constants import DbInfo; print(DbInfo.NAME.value)')
DB_PASSWORD = $(shell python3 -c 'from tdv.constants import DbInfo; print(DbInfo.PASSWORD.value)')
DB_HOST = $(shell python3 -c 'from tdv.constants import DbInfo; print(DbInfo.HOST.value)')
ALEMBIC_PATH = $(shell python3 -c 'from tdv.constants import ALEMBIC_DIR_PATH; print(ALEMBIC_DIR_PATH)')
VENV_ACTIVATE = venv/bin/activate


.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9_ -]+:.*#' Makefile | \
        awk 'BEGIN {FS = ":.*#"}; {printf "\033[1;32m%-30s\033[00m\t%s\n", $$1, $$2}'

init: venv req build psql_install db_user create_db db_up  # Run all the commands necessary to set up the environment

venv: del_venv  # Delete old venv & make a new one
	- python3 -m venv venv

del_venv: # Delete venv
	- rm -rf venv

req:  # Install all packages listed in requirements.txt
	 - . venv/bin/activate && pip install -r requirements.txt

build: wreck # Build the project to be able to run the cli. Also deletes previous build if any.
	- . venv/bin/activate && pip install -e .

wreck:  # Deletes the build created with setup.py
	- rm -rf *.egg-info
	- . venv/bin/activate && pip uninstall -y $(shell python3 -c 'from tdv.constants import BUILD_NAME; print(BUILD_NAME)')

psql_install:  # Download & install PostgreSQL (Only valid for Ubuntu)
	- sudo apt update && sudo apt install postgresql postgresql-contrib

db_user:  # Create a psql user
	- sudo -u postgres psql -c "CREATE USER $(DB_USER) WITH PASSWORD '$(DB_PASSWORD)';"

create_db:  # Create a psql DB for this project
	- sudo -u postgres psql -c "CREATE DATABASE $(DB_NAME) OWNER $(DB_USER);"

db:  # Log into db shell
	- psql $(DB_NAME)

db_up:  # Run all alembic migration scripts to create all tables in DB
	- . venv/bin/activate && cd $(ALEMBIC_PATH) && alembic upgrade head

db_auto_rev:  # Autogenerate a new alembic revision with arg REV, i.e make db_rev REV=add_table...
	- . venv/bin/activate && cd $(ALEMBIC_PATH) && alembic revision --autogenerate -m "$(REV)"

db_rev:  # Create an empty alembic revision with arg REV, i.e make db_rev REV=add_table...
	- . venv/bin/activate && cd $(ALEMBIC_PATH) && alembic revision -m "$(REV)"

db_hist:  # Print alembic revision history
	- . venv/bin/activate && cd $(ALEMBIC_PATH) && alembic history

db_down:  # DANGER! Run downgrade script to revert most recent revision, will DELETE ALL DATA in that table
	- . venv/bin/activate && cd $(ALEMBIC_PATH) && alembic downgrade -1

db_down_all:  # EXTREME DANGER! Deletes all tables in DB, will DELETE ALL DATA
	- . venv/bin/activate && cd $(ALEMBIC_PATH) && alembic downgrade base

drop_db:  # EXTREME DANGER!! Destroys project DB, will DELETE ALL DATA
	- sudo -u postgres psql -c "DROP DATABASE $(DB_NAME);"

configs:  # Runs the parser found in tdv.common_utils to set the alembic.ini DB path
	- $(shell python3 -c 'from tdv.common_utils import config_parser; config_parser()')

fmt:  # Run black with appropriate char limit
	- sudo black --line-length 128 --skip-string-normalization .

clean:  # Remove compiled Python files, cached directories & build artifacts
	- find . -name \*.pyc -delete
	- find . -depth -name __pycache__ -exec rm -rf {} \;
	- rm -rf *.egg-info
	- rm -rf dist/
	- rm -rf build/
	- rm -rf .eggs
