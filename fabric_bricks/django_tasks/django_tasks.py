from fabric.api import cd, task, require
from fabric.state import env
from fabric_bricks.utils import execute, virtualenv


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


@task
def collect_static():
    from django.conf import settings

    require('root', provided_by=('An environment task'))
    with cd(env.root):
        with virtualenv():
            execute('./manage.py collectstatic --noinput --settings=%(settings)s' % env)
            if 'compress' in settings.INSTALLED_APPS:
                execute('./manage.py compress --force --settings=%(settings)s' % env)

