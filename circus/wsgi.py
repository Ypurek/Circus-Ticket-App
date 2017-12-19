"""
WSGI config for circus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/opt/bitnami/apps/django/django_projects/cirucs')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/circus/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "circus.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
