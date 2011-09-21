from fabric.decorators import task
from fabric.operations import local
import os
from fabric_bricks.utils import packages_ensure
import settings

@task
def ensure():
    """
    Install all required packages of mysql.
    """

    packages_ensure(['sqlite'])


@task
def clear():
    """
    Recreate de db schema.
    """

    file_name = settings.DATABASES['default']['NAME']

    if os.path.exists(file_name):
        local('rm %s' % file_name)

