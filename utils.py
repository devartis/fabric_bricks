from cuisine.cuisine import package_ensure
from fabric.operations import run

def packages_ensure(packages):
    for package in packages:
        package_ensure(package)


def is_package_installed(package_name):
    status = run("dpkg-query -W -f='${Status}' %s ; true" % package_name)

    return not (status.find("installed") == -1 or status.find("unknown ok") != -1)