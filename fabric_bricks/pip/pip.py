from fabric.api import task, abort, require, cd
from fabric.state import env
from fabric_bricks.utils import execute, virtualenv


@task
def install(package=None, version_str=" "):
    """
    Install a pip package.
    """
    if not package:
        abort('Provide a package name and optionally a version. Example: fab %(command)s:package=django,version===1.2' % env)

    with virtualenv():
        execute('pip install %s%s' % (package, version_str))
        execute('pip freeze > requirements.txt')


@task
def uninstall(package=None):
    """
    Uninstall a pip package.
    """
    if not package:
        abort('Provide a package name. Example: fab %(command)s:package=django' % env)

    with virtualenv():
        execute('pip uninstall %s' % package)
        execute('pip freeze > requirements.txt')


@task
def install_dependencies():
    """
    Install dependencies defined in requirements.txt
    """
    require('root', provided_by=('An environment task'))
    with cd(env.root):
        with virtualenv():
            execute('pip install -r requirements.txt')
