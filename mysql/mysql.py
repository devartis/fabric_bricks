from fabric.decorators import task
from fabric.operations import local
from fabric_bricks.utils import packages_ensure
from fabric_bricks.config import *

@task
def ensure():
    """
    Install all required packages of mysql.
    """

    packages_ensure(['mysql-server', 'mysql-client', 'libmysqlclient15-dev'])


@task
def backup():
    """
    Create a backup of the db.
    """
    ensure()

    raise NotImplementedError


@task
def download_last_backup():
    """
    download the last backup.
    """

    raise NotImplementedError

@task
def drop_schema():
    local('mysql -u%(mysql_user)s -e "DROP SCHEMA IF EXISTS %(mysql_db_name)s"' % {
        "mysql_user": mysql_user,
        "mysql_pass": mysql_pass,
        "mysql_db_name": mysql_db_name,
        })


@task
def create_schema():
    local('mysql -u%(mysql_user)s -e "CREATE SCHEMA %(mysql_db_name)s"' % {
        "mysql_user": mysql_user,
        "mysql_pass": mysql_pass,
        "mysql_db_name": mysql_db_name,
        })


def clear():
    """
    Recreate de db schema.
    """

    drop_schema()
    create_schema()
