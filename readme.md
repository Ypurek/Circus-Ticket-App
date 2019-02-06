# How To Run Locally

* Install Python
* Create virtual environment
* Install dependencies: `pip install -r requirements.txt`
* Install DB (postgres)
* Set DB credentials in circus/settings.py
* Run: `manage.py makemigrations core`
* Run: `manage.py migrate`
* Run: `manage.py createsuperuser`
* Run: `manage.py runserver`
* Set default DB values by accessing 127.0.0.1:8000/ws/auto/settings

# Ho to deploy on Ubuntu 18 (postgress, gunicorn, nginx)
Guide - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04


# (OLD) Ho to deploy on Linux server (Bitnami)
* Remove another django projects (it is simple way. Or check https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/modwsgi/)
* Upload project
* Configure according to https://docs.bitnami.com/google/infrastructure/django/?utm_source=bitnami&utm_medium=cloudimage&utm_campaign=google
* In httpd.conf set: Alias /assets /opt/bitnami/apache2/htdocs/assets to make static files available
* Execute steps 3,5-10 of Install list
* setup crontab https://pypi.python.org/pypi/django-crontab
* Run: `manage.py crontab add`
* Run to check: `manage.py crontab show`
* Follow https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
