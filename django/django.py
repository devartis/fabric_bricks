from fabric.decorators import task
from fabric.contrib.files import upload_template
from fabric.operations import local
from fabric_bricks.config import *

settings_source = 'fabric_bricks/django/conf/settings.py'
settings_destination = project_dir + 'settings.py'

wsgi_source = 'fabric_bricks/django/conf/wsgi.py'

@task
def copy_production_settings():
    """
    Copy Production settings.py to site.
    """

    upload_template(settings_source, settings_destination, backup=False,
                    context={
                        'db_name': mysql_db_name,
                        'db_user': mysql_user,
                        'db_pass': mysql_pass,
                        'server_ip': server_ip,
                        'static_dir': static_dir,
                        })

@task
def copy_wsgi_config():
    """
    Copy wsgi script.
    """

    upload_template(wsgi_source, site_wsgi_path, backup=False,
                    context={
                        'virtual_env_site_packages': virtual_env_dir,
                        'project_dir': project_dir,
                        'project_name': django_project_name,
                        })

def syncdb():
    local('./manage.py syncdb --noinput')