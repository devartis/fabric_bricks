from fabric.api import local, task
from fabric_bricks.django.django import syncdb, dropdb
from fabric_bricks.utils import execute


def using_sqlite():
    from django.conf import settings
    return settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3'


@task
def recreate_db():
    """
    Recreate the db schema.
    """
    from django.conf import settings
    dropdb(settings.INSTALLED_APPS)
    syncdb(settings.INSTALLED_APPS)


@task
def unit_tests():
    """
    Run unit tests.
    """
    from django.conf import settings
    for app in settings.APP_MODULES:
        execute('nosetests -w %s/tests/unit' % app)


@task
def integration_tests():
    """
    Run integration tests.
    """
    from django.conf import settings
    for app in settings.APP_MODULES:
        execute('nosetests -w %s/tests/integration' % app)


@task
def acceptance_tests():
    """
    Run acceptance tests.
    """
    from django.conf import settings
    for app in settings.APP_MODULES:
        execute('nosetests -w %s/tests/acceptance' % app)


@task
def all_tests():
    """
    Run all tests.
    """

    local('nosetests')
