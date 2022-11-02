# Circus Ticket App

By QA Mania  
- https://qamania.org
- https://t.me/qamania
- https://www.youtube.com/c/qamania

## About
This is new life of application for students who want to be a QA. It was initially developed in 2017 ⚠️
to be tested by students, find bugs and report them.  
There are about 20+ bugs hidden inside ;)
⚠️⚠️This app was the very first Djano app I've created so the code is bad and dirty. Really.
I'm surprised I could update it and make run locally so quickly. 
I don;t have a plan to refactor the code to make it pretty as it is working 😂

## Application Description
Circus Ticket App - system to view, book and buy tickets to circus.  
There is SRS created to cover all its requirements in Google Docs: [Link here](https://docs.google.com/document/d/1WK2YVN73e1pl2pO4FwWM8r5aW1lCzHheBPEOy8lONyI/edit?usp=sharing) 

## Try it online!
 - Circus http://circus.qamania.org/
 - Circus testing pages http://circus.qamania.org/testing/

## Release notes

### 1.3.0
 - added jobs to clean old discount codes, credit cards, ticket history once per month
 - added ws to clear old stuuf above by using `<app_url>/ws/auto/clear`

### 1.2.0
 - removed old cron scheduler and added new one, working on Windows now
 - removed Apache configs. Now only nginx!
 - Set default DB SQLite to make app run locally easy
 - set default configs to migrations
 - set default data to migrations with tickets for 2035 year
 - added db to repo to let app run right after clone

### 1.0.0 
 - complicated registration and login
 - anonymous login with limited functionality
 - dashboard with ability to search and filter tickets
 - shopping cart with complicated additional ticket options
 - personal info screen
 - test pages to manage credit cards, discount coupons and track tickets history (access by `<app_url>/testing` link)
 - bugs in different features

## API
[API docs in Postman](https://documenter.getpostman.com/view/2037649/circus/RVuAC6pM)

## Preconditions
- Python 3.10+
- Install dependencies using `pip install -r requirements.txt`
- Free network port 8000

## How to run locally
1. Open CLI
2. Navigate to project folder
3. Execute command: `python manage.py runserver`  

Server will be started at http://127.0.0.1:8000  

## Ho to deploy on Ubuntu 18 (postgress, gunicorn, nginx)
Guide - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

## Notes ⚠️
Initially app was developed to use PostgreSQL, but now, to make it easier to run locally, I've decided to switch 
it back to SQLite.
Check configs in commits if you want PostgreSQL configs back
  
Have fun with testing ❤️
