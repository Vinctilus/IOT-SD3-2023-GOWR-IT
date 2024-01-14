# flask_app.wsgi
import sys
import logging 
import os
sys.path.insert(0, '/var/www/FlaskApp/')
os.environ["Test"]='test'
def application(environ, start_response):
	for key in ['Test']:
		os.environ[key] = environ.get(key,'')
	from FlaskApp import app as _application
	_application.secret_key='secret'
	return _application(environ, start_response)


