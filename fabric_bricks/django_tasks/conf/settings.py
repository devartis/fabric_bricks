from settings_base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '%(db_name)s',
            'USER': '%(db_user)s',
            'PASSWORD': '%(db_pass)s',
            'OPTIONS': {
                "init_command": "SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED"
            }
        },
}

MEDIA_URL = 'http://%(server_ip)s/static/'
STATIC_URL = "http://%(server_ip)s/static/"
ADMIN_MEDIA_PREFIX = 'http://%(server_ip)s/static/admin/'
STATIC_ROOT = '%(static_dir)s'

MEDIA_ROOT = '%(static_dir)s'
PICTURES_DIR = MEDIA_ROOT + "pictures/"

APP_ID = '119600283531'
APP_SECRET = 'd397d419de453bc70ab87a2f8bc40b17'
APP_SCOPE = 'email,read_stream,offline_access,publish_stream'
