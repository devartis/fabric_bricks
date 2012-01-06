from fabric.api import task
from fabric_bricks.utils import packages_ensure, execute
import os


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
    from django.conf import settings
    file_name = settings.DATABASES['default']['NAME']

    if os.path.exists(file_name):
        execute('rm %s' % file_name)
