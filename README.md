Contact Lists
=============

Contact Lists is a simple web app that will let you store contacts.

App is being built using Django REST Framework for API and AngularJS for the front end. 


How to run this project?
========================

1. Make sure you have installed PostgreSQL and setup your database.

Follow this guide: https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04

2. Modify the file: /contactlists/config/settings/base.py with your database's credentials.

3. Then execute these commands from terminal.

>virtualenv venv
>source venv/bin/activate
>pip install -U pip
>pip install -r requirements.txt 
>cd $DIR_PATH #your project directory
>python3 manage.py migrate
>python3 manage.py runserver

4. Browse the site by this address: http://127.0.0.1:8000/


