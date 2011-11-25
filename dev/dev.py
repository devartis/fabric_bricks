from fabric.api import local, task
from fabric_bricks.django.django import syncdb, dropdb
from fabric_bricks.utils import virtualenv

def using_sqlite():
    from django.conf import settings
    return settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3'


@task
def recreate_db():
    """
    Recreate the db schema.
    """
    from django.conf import settings
    with virtualenv():
        dropdb(settings)
        syncdb()


@task
def unit_tests():
    """
    Run unit tests.
    """
    local('nosetests -w user_profile/tests/unit')


@task
def integration_tests():
    """
    Run integration tests.
    """

    local('nosetests -w user_profile/tests/integration')
    local('nosetests -w hotels/tests/integration')


@task
def acceptance_tests():
    """
    Run acceptance tests.
    """

    local('nosetests -w user_profile/tests/acceptance')


@task
def all_tests():
    """
    Run all tests.
    """

    local('nosetests')
