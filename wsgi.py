import os
import sys

path = '/home/YOUR_PYTHONANYWHERE_USERNAME/fcm_django'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'fcm_django.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
