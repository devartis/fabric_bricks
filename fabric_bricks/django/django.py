from fabric.context_managers import cd
from fabric.decorators import task
from fabric.contrib.files import upload_template
from fabric.state import env

from fabric_bricks.utils import execute, virtualenv

settings_source = 'fabric_bricks/django/conf/settings.py'
wsgi_source = 'fabric_bricks/django/conf/wsgi.py'

@task
def copy_production_settings():
    """
    Copy Production settings.py to site.
    """

    upload_template(settings_source, env.root + 'settings.py', backup=False,
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

def dropdb(apps):
    for app in apps:
        with cd(env.root):
            with virtualenv():
                execute('./manage.py sqlclear %s | ./manage.py dbshell' % app)

def syncdb():
    with cd(env.root):
        with virtualenv():
            execute('./manage.py syncdb --noinput --settings=%(settings)s' % env)

            
def collect_static():
    with cd(env.root):
        with virtualenv():
            execute('./manage.py collectstatic --noinput')