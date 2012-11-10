from django.core.management import setup_environ
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.models import User
import requests, pymongo, datetime, sys

#sys.path.insert(0, '../web_app/')
sys.path.insert(0, '../')

import settings
setup_environ(settings)
from web_app.models import * 



print "Hello World"
