from cuisine.cuisine import package_ensure
from fabric.context_managers import prefix
from fabric.api import run, local
from fabric.operations import require
from fabric.state import env

def packages_ensure(packages):
    for package in packages:
        package_ensure(package)


def is_package_installed(package_name):
    status = run("dpkg-query -W -f='${Status}' %s ; true" % package_name)

    return not (status.find("installed") == -1 or status.find("unknown ok") != -1)

def execute(*args, **kwargs):
    if env.remote:
        run(*args, **kwargs)
    else:
        local(*args, **kwargs)

def virtualenv():
    require('virtual_env_name')

    if not env.remote:
        return prefix('echo')

    with prefix('export WORKON_HOME=~/python_envs'):
        with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
            return prefix('workon %(virtual_env_name)s' % env)

