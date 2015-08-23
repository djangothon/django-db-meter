"""
WSGI config for test_meter project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

APP_ROOT = os.path.abspath(os.path.dirname(__file__))
print APP_ROOT
sys.path.insert(0, APP_ROOT)
APP_ROOT_PREV = os.path.join(APP_ROOT, '..')
APP_ROOT_PREV = os.path.abspath(APP_ROOT_PREV)
sys.path.insert(0, APP_ROOT_PREV)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_meter.settings")

application = get_wsgi_application()
