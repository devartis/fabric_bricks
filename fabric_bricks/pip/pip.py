from fabric.decorators import task
from fabric.operations import local
from fabric.utils import abort


@task
def install(package=None, version_str=" "):
    """
    Install a pip package.
    """

    if not package:
        abort('provide name and optionally a version. Example: fab pip.install:package=django,version===1.2')

    local('pip install %s%s' % (package, version_str))
    local('pip freeze > requirements.txt')


@task
def uninstall(package=None):
    """
    Uninstall a pip package.
    """

    local('pip uninstall %s' % package,)
    local('pip freeze > requirements.txt')