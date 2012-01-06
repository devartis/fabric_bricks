from cuisine.cuisine import package_ensure
from fabric.contrib.files import upload_template
from fabric.decorators import task
from fabric.operations import sudo
from fabconfig import *

site_conf_source = 'fabric_bricks/nginx/conf/nginx-site.conf'
site_conf_destination = '/etc/nginx/sites-enabled/travtar'

gral_conf_source = 'fabric_bricks/nginx/conf/nginx.conf'
gral_conf_destination = '/etc/nginx/nginx.conf'

proxy_conf_source = 'fabric_bricks/nginx/conf/nginx-proxy.conf'
proxy_conf_destination = '/etc/nginx/proxy.conf'


@task
def ensure():
    """
    Install all required packages of nginx.
    """
    package_ensure('nginx')


def copy_site_config():
    upload_template(site_conf_source, site_conf_destination, use_sudo=True, backup=False,
                    context={
                        'port': nginx_port,
                        'server_ip': server_ip,
                        'logs_dir': logs_dir,
                        'proxy_pass_url': nginx_proxy_pass_url,
                        'proxy_pass_port': nginx_proxy_pass_port,
                        'proxy_conf_path': proxy_conf_destination,
                        'media_dir': site_dir,
                        'static_dir': site_dir,
                        })


def copy_gral_config():
    upload_template(gral_conf_source, gral_conf_destination, use_sudo=True, backup=False)


def copy_proxy_config():
    upload_template(proxy_conf_source, proxy_conf_destination, use_sudo=True, backup=False)


@task
def configure():
    """
    Configure the nginx web server.
    """
    ensure()

    copy_site_config()
    copy_gral_config()
    copy_proxy_config()


@task
def start():
    """
    Start the nginx web server.
    """
    sudo('ngnix')


@task
def restart():
    """
    Restart the nginx web server.
    """
    stop()
    start()


@task
def stop():
    """
    Stop the nginx web server.
    """
    sudo('ngnix -s stop')
