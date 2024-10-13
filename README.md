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
>  - Docker 24.0.5
> 
> It allows you to view the quantoty left on each stock, Allows users to issue new stock with different types of transaction types, view all transactions and also from the admin page the user is able to edit some tables from the database using in place table edits and ajax-POST requests


## Installation (Docker):

**1. Configuration file:**
> Copy the `configfile` from `setup_files` into StockTaking folder next to `manage.py`
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


## Installation (Manual Linux):

**1. Configuration file:**
> Copy the `configfile` from `setup_files` into StockTaking folder next to `manage.py``
> Rename this file to `config.ini`
> Alter the content of the file to suit your MySQL server settings
> ```
> [database]
> database=<database name>
> user=<username>
> password=<user password>
> host=<host(default:localhost)>
> port=<port(default:3306)>
> ```

**2. Database Test Data:**
> Run the `test_data.sql` file in the `setup_files` folder on your MySQL server to create the database and add some test data.
> You can use the following command to run the file:
> `mysql -u <username> -p < test_data.sql`
> *NOTE:* This is not required but it will make it easier to test the application.

**3. Virtual Environment:**
> Create a virtual environment in the same directory as `manage.py` using the command:
> `python -m venv venv`
> Activate the virtual environment using:
> `source venv/bin/activate`
> Install the required packages using:
> `pip install -r requirements.txt`
> *NOTE:* If you are using a different version of python, you might need to install the packages manually using:
> `pip install <package name>`

**4. Settings.py:**
> In the `settings.py` file in `StockTaking/StockTaking` scroll down to the `ALLOWED_HOSTS = []`
> Change this line to `ALLOWED_HOSTS = ['*']`
> *NOTE:* This is to allow the server to be accessed from any host.

**5. Migrations:**
> Navigate to the `StockTaking` folder.
> Run migrations on the Django database to get access to sessions and other django components.
> Run:
> `python manage.py migrate`
> *NOTE:* If you are using a different version of python, you might need to run the migrations manually using:
> `python manage.py makemigrations`
> `python manage.py migrate`

**6. Run Server:**
> Run the server using:
> `python manage.py runserver`
> Test the server on `localhost:8000`
