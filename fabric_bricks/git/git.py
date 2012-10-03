from fabric.api import task, require, cd
from fabric.state import env
from fabric_bricks.utils import execute


@task
def pull(tags=False):
    """
    Pulls latest changes from Git
    """
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        execute('git pull %s' % ('i--tags' if tags else ''))


@task
def checkout(name):
    """
    Checkouts the given tag or branch
    """
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        execute('git checkout %s' % name)
