# Stock Taking

## Overview:
> This is a simple stock taking application that allows users to manage different types of stock. The app will have 3 main components: User sessions, Database management, and Stock management. 
> <br/>
> **Technologies**:
>  - Python 3.10.12
>  - Django 4.2.7
>  - MySQL
>  - JQuery - Ajax
>  - In-Place Editing
>
> It allows you to view the quantoty left on each stock, Allows users to issue new stock with different types of transaction types, view all transactions and also from the admin page the user is able to edit some tables from the database using in place table edits and ajax-POST requests


## Installation

**1. Configuration file:**
> Copy the `configfile` from `setup_files` into StockTaking folder next to `manage.py``
> Rename this file to `config.ini`  


**2. Docker Compose:**
> Run `docker-compose up` optionally add `-d` flag to run in background
> *NOTE:* This might give an error at first related to the django server not being able to connect to 'db', this is due to the 'db' server taking a while to start up. Do not mind this eeror as the next step should resolve it.

**3. Settings.py:**
> In the `settings.py` file in `StockTaking/StockTaking` scroll down to the `ALLOWED_HOSTS = []` 
> Change this line to `ALLOWED_HOSTS = ['*']`

**4. Migrations:**
> Run migrations on the Django database to get access to sessions and other django components.
> Open another terminal window in the same directory and run:
> `docker-compose run --rm web python StockTaking/manage.py migrate`

> Test the server on `localhost:8000`
