from fabric.decorators import task
from fabric.operations import local
from fabric_bricks.utils import packages_ensure
from fabconfig import *


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
    pass_parameter = ("-p" + mysql_pass) if mysql_pass != "" else ""
    local('mysql -u%(mysql_user)s %(pass_parameter)s -e "DROP SCHEMA IF EXISTS %(mysql_db_name)s"' % {
        "mysql_user": mysql_user,
        "pass_parameter": pass_parameter,
        "mysql_db_name": mysql_db_name,
        })


@task
def create_schema():
    pass_parameter = ("-p" + mysql_pass) if mysql_pass != "" else ""
    local('mysql -u%(mysql_user)s %(pass_parameter)s -e "CREATE SCHEMA %(mysql_db_name)s"' % {
        "mysql_user": mysql_user,
        "pass_parameter": pass_parameter,
        "mysql_db_name": mysql_db_name,
        })


def clear():
    """
    Recreate de db schema.
    """

    drop_schema()
    create_schema()
