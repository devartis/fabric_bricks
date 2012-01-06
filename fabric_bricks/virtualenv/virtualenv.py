from fabric.contrib.files import append, exists
from fabric.decorators import task
from fabric.operations import run, sudo
from fabric.context_managers import prefix, cd
from fabconfig import *
from fabric_bricks.utils import *


def install_pip():
    package_ensure("python-pip")


def install_virtual_env_wrapper():
    sudo('pip install virtualenvwrapper')

    if exists(virtual_envs_dir):
        return

    run('mkdir %s' % virtual_envs_dir)
    append('~/.bashrc', 'export WORKON_HOME=%s' % virtual_envs_dir)
    append('~/.bashrc', 'source $(which virtualenvwrapper.sh)')
    run('source ~/.bashrc')


def create_virtual_env_dir():
    if exists(virtual_env_dir):
        return

    with prefix('export WORKON_HOME=%s' % virtual_envs_dir, ):
        with prefix('source $(which virtualenvwrapper.sh)'):
            run('mkvirtualenv --no-site-packages  %s' % virtual_env_name)
            with prefix('workon %s' % virtual_env_name, ):
                run('add2virtualenv %s' % site_dir)

    run('echo "export DJANGO_SETTINGS_MODULE=%s.settings" > %spostactivate' % (django_project_name, virtual_envs_dir))


@task
def ensure():
    install_pip()
    install_virtual_env_wrapper()
    create_virtual_env_dir()


@task
def create():
    raise NotImplementedError


def work_on():
    return 'workon %(virtual_env_name)s' % env


def virtual_env_site_packages_dir():
    with prefix(work_on()):
        return run('python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"')
