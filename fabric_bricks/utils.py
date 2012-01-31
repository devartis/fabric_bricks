from random import Random
from cuisine.cuisine import package_ensure
from fabric.context_managers import prefix
from fabric.api import run, local, require, prompt
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

    if not hasattr(env, 'virtual_env_workon_home'):
        workon_home = '~/python_envs'
    else:
        workon_home = env.virtual_env_workon_home

    with prefix('export WORKON_HOME=%s' % workon_home):
        with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
            return prefix('workon %(virtual_env_name)s' % env)


def strong_confirm(msg):
    x = Random().randint(10, 30)
    y = Random().randint(10, 30)
    z = str(x + y)
    if msg:
        response = prompt("%s\nTo continue solve this %d + %d:" % (msg, x, y)).lower().strip()
    else:
        response = prompt("To continue solve this %d + %d:" % (x, y)).lower().strip()

    if response in ['no', 'n']:
        return False

    if response == z:
        return True

    print("Wrong answer! Please specify the correct answer or '(n)o'.")
    return strong_confirm(None)
