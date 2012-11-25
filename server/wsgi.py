import os
import sys

#NOTE: the following path needs to be changed appropriately
sys.path.append('/home/ec2-user/ActiveOulu/')
sys.path.append('/home/ec2-user/ActiveOulu/server/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.

#Django 1.4
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

#Django 1.3
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
