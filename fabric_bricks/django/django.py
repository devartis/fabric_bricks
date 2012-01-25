from fabric.state import env
from fabric.api import cd, task, require
from fabric.contrib.files import upload_template

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
    # Invert apps to avoid dependency problems.
    apps = list(apps)
    apps.reverse()

    failed_apps = []

    for app in apps:
        app = app.split('.')[-1]
        with cd(env.root):
            with virtualenv():
                try:
                    # We need to split DROP TABLEs from DROP FK because MySQL aborts if the FK doesn't exists
                    try:
                        execute('./manage.py sqlclear %(app)s --settings=%(settings)s | grep "DROP FOREIGN KEY" | ./manage.py dbshell --settings=%(settings)s' % {'app': app, 'settings': env.settings})
                    except:
                        # Ignore errors while dropping FK.
                        pass
                    execute('./manage.py sqlclear %(app)s --settings=%(settings)s | grep "DROP TABLE" | ./manage.py dbshell --settings=%(settings)s' % {'app': app, 'settings': env.settings})
                except:
                    failed_apps.insert(0, app)

    if failed_apps:
        dropdb(failed_apps)


def syncdb(apps, initial_data=False):
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        with virtualenv():
            execute('./manage.py syncdb --noinput --settings=%(settings)s' % env)
    if 'south' in apps:
        migrate(initial_data)


def migrate(initial_data=False):
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        with virtualenv():
            if initial_data:
                execute('./manage.py migrate --settings=%(settings)s' % env)
            else:
                execute('./manage.py migrate --no-initial-data --settings=%(settings)s' % env)


def collect_static():
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        with virtualenv():
            execute('./manage.py collectstatic --noinput --settings=%(settings)s' % env)

