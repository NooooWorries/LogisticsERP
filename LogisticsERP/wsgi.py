"""
WSGI config for LogisticsERP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import site
site.addsitedir('/usr/local/lib/python3.6/site-packages')

import os
from os.path import join,dirname,abspath
PROJECT_DIR = "/var/www/LogisticsERP/"

import sys
sys.path.insert(0, PROJECT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LogisticsERP.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
