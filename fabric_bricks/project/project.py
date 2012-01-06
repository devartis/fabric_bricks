from fabric.decorators import task
from fabric.operations import run
from fabric.contrib.files import exists
from fabconfig import *


@task
def create_working_directory():
    """Creates the directories for the site."""

    if not exists(site_dir):
        run("mkdir %s" % site_dir)

    if not exists(project_dir):
        run("mkdir %s" % project_dir)

    if not exists(project_dir):
        run("mkdir %s" % static_dir)

    if not exists(backups_dir):
        run("mkdir %s" % backups_dir)

    if not exists(logs_dir):
        run("mkdir %s" % logs_dir)


@task
def add_web_server_perms_to_site_dir():
    """
    Add web-server perms to site directory.
    """
    raise NotImplementedError
