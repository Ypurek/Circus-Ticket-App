import os, sys

sys.path.append('/opt/bitnami/apps/django/django_projects/circus')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/circus/egg_cache")
os.environ["DJANGO_SETTINGS_MODULE"] = "circus.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
