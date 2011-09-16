from cuisine.cuisine import user_check, user_create, group_user_add
from fabric.decorators import task
from fabric.utils import abort
from fabric_bricks.config import *


@task
def create_devartis_user(user=None, password=None):
    """
    Create a sudo-user in web-sever group.
    """
    if user is None or password is None:
        abort('Provide me a user and password. Like "fab create_devartis_user:user=diego,password=lala"')

    user_name = env.user
    user_pass = env.password

    env.user = user
    env.password = password
    
    if not user_check(user_name):
        user_create(user_name, user_pass, shell='/bin/bash')
        group_user_add(admin_group, user_name)

