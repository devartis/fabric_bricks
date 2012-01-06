from fabric.contrib.files import upload_template, contains, append
from fabric.decorators import task
from fabric.operations import sudo
from fabric_bricks.utils import packages_ensure
from fabconfig import *

config_source = 'fabric_bricks/apache/conf/virtual-host.conf'
config_destination = '/etc/apache2/sites-enabled/001-travtar'

httpd_conf_path = '/etc/apache2/httpd.conf'


@task
def ensure():
    """
    Install all required packages of apache.
    """
    packages_ensure(["apache2", "apache2.2-common",
                     "apache2-mpm-worker", "apache2-threaded-dev",
                     "libapache2-mod-wsgi", "python-dev"])


def copy_virtual_host_config():
    upload_template(config_source, config_destination, use_sudo=True, backup=False, context={
        'port': apache_port,
        'server_name': apache_server_name,
        'site_wsgi_path': site_wsgi_path,
        'logs_dir': logs_dir,
        })


def set_server_name():
    if not contains(httpd_conf_path, 'ServerName .*$'):
        append(httpd_conf_path, 'ServerName localhost', use_sudo=True)


@task
def configure():
    """
    Configure the apache virtual host.
    """
    ensure()

    copy_virtual_host_config()
    set_server_name()


@task
def start():
    """
    Start the apache web server.
    """
    sudo('apachectl start')


@task
def restart():
    """
    Restart the apache web server.
    """
    sudo('apachectl restart')


@task
def stop():
    """
    Stop the apache web server.
    """
    sudo('apachectl stop')


@task
def restart_gracefully():
    """
    Restart the apache web server gracefully.
    """
    sudo('apachectl graceful')
