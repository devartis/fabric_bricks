from fabric.api import cd, task, require
from fabric.state import env
from fabric_bricks.utils import execute, virtualenv


def dropdb():
    # Invert apps to avoid dependency problems.
    from django.conf import settings
    apps = list(settings.INSTALLED_APPS)
    apps.reverse()

    failed_apps = []

    for app in apps:
        app = app.split('.')[-1]
        with cd(env.root):
            with virtualenv():
                try:
                    # We need to split DROP TABLEs from DROP FK because MySQL aborts if the FK doesn't exists
                    try:
                        execute('python manage.py sqlclear %(app)s --settings=%(settings)s | grep "DROP FOREIGN KEY" | ./manage.py dbshell --settings=%(settings)s' % {'app': app, 'settings': env.settings})
                    except:
                        # Ignore errors while dropping FK.
                        pass
                    execute('python manage.py sqlclear %(app)s --settings=%(settings)s | grep "DROP TABLE" | ./manage.py dbshell --settings=%(settings)s' % {'app': app, 'settings': env.settings})
                except:
                    failed_apps.insert(0, app)

    if failed_apps:
        dropdb(failed_apps)


def syncdb(initial_data=False):
    from django.conf import settings
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        with virtualenv():
            execute('python manage.py syncdb --noinput --settings=%(settings)s' % env)
    if 'south' in settings.INSTALLED_APPS:
        migrate(initial_data)


def migrate(initial_data=False):
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        with virtualenv():
            if initial_data:
                execute('python manage.py migrate --settings=%(settings)s' % env)
            else:
                execute('python manage.py migrate --no-initial-data --settings=%(settings)s' % env)


def rebuild_index():
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        with virtualenv():
            execute('python manage.py rebuild_index --noinput --settings=%(settings)s' % env)


def collect_static():
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        with virtualenv():
            execute('python manage.py collectstatic --noinput --settings=%(settings)s' % env)


def compress():
    from django.conf import settings

    require('root', provided_by=('An environment task'))
    with cd(env.root):
        with virtualenv():
            if 'compressor' in settings.INSTALLED_APPS:
                execute('python manage.py compress --force --settings=%(settings)s' % env)

