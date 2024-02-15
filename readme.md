# Trading Data Visualizer, TDV

Project to retrieve market data from yahoofinance, store and serve to client


## Project setup:

Designed to work in Linux, tested on Ubuntu22, must install python3, tested on python3.10


### Easy setup with Makefile:
    make all
For this to work you must have python3.10 on path, venv module installed and pip, since 
it will create a new venv, install all  dependencies, run setup.py, declare system  
variables, install psql, log into psql, create your user, create the database, log 
out of psql, run the migration scripts to create the tables in the database and 
make you a sandwich ;)

### Harder setup:
You can explore the Makefile and run only specific commands, or do all the above manually,
or a combination.
