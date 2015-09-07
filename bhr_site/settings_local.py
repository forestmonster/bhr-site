LOCAL_SETTINGS = True  # do not touch
from settings import * # do not touch

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'computer2', u'192.168.1.131', u'192.168.56.101']
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

#STATIC_ROOT="/home/forest/bhr/static"
STATIC_ROOT="/home/forest/bhr-site/bhr/static/"

ADMINS = (("forest", "forest@localhost"), )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bhr',
	'USER': 'bhr',
	'HOST': 'localhost',
	'PASSWORD': 'bhr'
    }
}

BHR = {
    'time_multiplier':              2.0,
    'time_window_factor':           2.0,
    'minimum_time_window':          43200.0,
    'penalty_time_multiplier':      2.0,
    'return_to_base_multiplier':    2.0,
    'return_to_base_factor':        2.0,
}
