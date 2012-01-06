from fabric.api import task, require, cd
from fabric.state import env
from fabric_bricks.utils import execute


@task
def pull():
    """
    Pulls latest changes from GIT
    """
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        execute('git pull')
