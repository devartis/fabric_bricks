from fabric.api import task, require, cd
from fabric.operations import local, run
from fabric.state import env
from fabric.utils import abort

from fabric_bricks.utils import execute

@task
def up():
    """
    Updates to the latest changes from SVN
    """
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        execute('svn up')

@task
def create_tag(tag=None):
    """
    Create an svn tag.
    """

    if tag is None:
        abort('Please, provide a tag to checkout. Like "fab create_tag:tag=0_1"')

    local('svn copy %(svn_base_dir)strunk %(svn_base_dir)s/tags/%(tag)s/ -m "Tag %(tag)s."' % {
        "svn_base_dir": svn_base_dir,
        "tag": tag,
        })


def get_latest_tag():
    tags = local('svn list %s/tags' % svn_base_dir)

    raise NotImplementedError


@task
def checkout(tag):
    """
    Do a checkout on the working directory.
    """

    run("svn export %(svn_tag_dir)s%(tag)s/ . --username  %(user)s  --no-auth-cache --force" % {
        "svn_tag_dir": svn_tag_dir,
        "tag": tag,
        "user": svn_user
        })

    raise NotImplementedError
