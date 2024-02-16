# Trading Data Visualizer, TDV

Project to retrieve market data from yahoofinance, store and serve to client


## Project setup:

Tested on Ubuntu22, must have python3 on path, tested in python3.10

### Easy setup with Makefile:
    make init

Run this command in the project root i.e ~/tdv

For this to work you must have python3 on path, venv module installed and pip, since 
it will create a new venv, install all dependencies in it, run setup.py, install psql,
create your user, create database and run the migration scripts to create tables.
Also, will ignore errors and keep going so there might be errors, check.

### Harder setup:
You can explore the Makefile and run only specific commands, or do all the above manually,
or a combination.


## Running the program
Must activate venv, i.e run: source venv/bin/activate 

All the stuff you might want to run is ran through the CLI. Having created a build for
the project the 