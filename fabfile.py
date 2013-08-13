from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import task

from ade25.fabfiles import project
from ade25.fabfiles.server import controls
from ade25.fabfiles import hotfix as hf

env.use_ssh_config = True
env.forward_agent = True
env.port = '22222'
env.user = 'root'
env.code_user = 'root'
env.prod_user = 'www'
env.webserver = '/opt/webserver/buildout.webserver'
env.code_root = '/opt/webserver/buildout.webserver'
env.host_root = '/opt/sites'

env.hosts = ['zope1']
env.hosted_sites = [
    'asg',
    'reiter',
    'teama3',
    'ahlt',
    'androschin',
    'dichtl',
    'existenz',
    'rms',
    'langer',
    'anna',
]

env.hosted_sites_locations = [
    '/opt/sites/asg/buildout.asg',
    '/opt/sites/reiter/buildout.reiter',
    '/opt/sites/teama3/buildout.teama3',
    '/opt/sites/ahlt/buildout.ahlt',
    '/opt/sites/androschin/buildout.androschin',
    '/opt/sites/dichtl/buildout.dichtl',
    '/opt/sites/existenz/buildout.existenz',
    '/opt/sites/rms/buildout.rms',
    '/opt/sites/langer/buildout.langer',
    '/opt/sites/anna/buildout.anna',
]


@task
def push():
    """ Push committed local changes to git """
    local('git push')


@task
def restart():
    """ Restart all """
    with cd(env.webserver):
        run('nice bin/supervisorctl restart all')


@task
def restart_nginx():
    """ Restart Nginx """
    controls.restart_nginx()


@task
def nginx(*cmd):
    """ Nginx (start|stop|status) command """
    with cd(env.webserver):
        run('nice bin/supervisorctl ' + ' '.join(cmd) + ' nginx')


@task
def restart_varnish():
    """ Restart Varnish """
    controls.restart_varnish()


@task
def restart_haproxy():
    """ Restart HAProxy """
    controls.restart_haproxy()


@task
def ctl(*cmd):
    """Runs an arbitrary supervisorctl command."""
    with cd(env.webserver):
        run('nice bin/supervisorctl ' + ' '.join(cmd))


@task
def supervisorctl(*cmd):
    """Runs an arbitrary supervisorctl command."""
    with cd(env.webserver):
        run('nice bin/supervisorctl ' + ' '.join(cmd))


@task
def deploy():
    """ Deploy current master to production server """
    push()
    controls.update()
    controls.build()


@task
def deploy_site():
    """ Deploy a new site to production """
    push()
    controls.update()
    controls.build()
    controls.reload_supervisor()


@task
def hotfix(addon=None):
    """ Apply hotfix to all hosted sites """
    hf.prepare_sites()
    hf.process_hotfix()
