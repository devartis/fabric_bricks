from fabric.decorators import task
from fabric.operations import local
from fabric_bricks.django.django import syncdb
from fabric_bricks.mysql.mysql import clear as mysql_clear
from fabric_bricks.sqlite.sqlite import clear as sqlite_clear
import settings


def using_sqlite(settings=settings):
    return settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3'


@task
def recreate_db():
    """
    Recreate the db schema.
    """

    if using_sqlite():
        sqlite_clear()
    else:
        mysql_clear()

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
