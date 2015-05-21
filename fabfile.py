from fabric.api import env, run, cd, prefix, sudo
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists
from contextlib import contextmanager as _contextmanager


# the user to use for the remote commands
env.user = 'root'

# the servers where the commands are executed
env.hosts = ['104.131.15.37']
env.root = '/root'
env.project = '%s/BizTest' % env.root
env.environment = '%s/BizTestEnv' % env.root
env.activate = 'source %s/bin/activate' % env.environment
env.forward_agent = True
env.node_version = 'v0.10.36'


@_contextmanager
def virtualenv():
    with cd(env.project):
        with prefix(env.activate):
            yield


@_contextmanager
def buildenv():
    with cd(env.root):
        yield


def deploy():
    if not exists('%s/launch.sh' % env.root):
        # We haven't installed anything yet
        sudo('aptitude update')
        sudo('aptitude -y upgrade')
        sudo('aptitude install -y nginx supervisor ruby python-virtualenv gcc make python-dev git wget curl make g++ libevent-dev '
             'python-setuptools memcached libmemcached-dev libxml2-dev libxslt1-dev postgresql-9.3 postgresql-server-dev-9.3')

    if not exists('%s/node' % env.root):
        run('wget http://nodejs.org/dist/{0}/node-{0}.tar.gz'.format(env.node_version))
        run('tar -xzf node-{}.tar.gz'.format(env.node_version))
        with cd('node-{}'.format(env.node_version)):
            run('./configure --prefix=%s/node' % env.root)
            run('make && make install')
        run('%s/node/bin/npm install -g grunt-cli' % env.root)

    if not exists(env.environment):
        with cd(env.root):
            run('virtualenv %s' % env.environment)

    rsync_project(
            remote_dir=env.project,
            local_dir='./',
            exclude=('*.pyc', 'config.py', '.git', '.gitignore', '.tmp', 'node_modules', '.idea', 'dist', 'alembic.ini', 'dist/index.html', 'app/scripts/config.js', 'app/index.html', 'bower_components'),
            )

    if not exists('/etc/supervisor/conf.d/biztest.conf'):
        sudo('cp %s/config/biztest-supervisor.conf /etc/supervisor/conf.d/biztest.conf' % env.project)
        sudo('supervisorctl reread')
        sudo('supervisorctl update')
        sudo('supervisorctl start biztest')

    if not exists('/etc/nginx/sites-enabled/biztest'):
        sudo('cp %s/config/biztest-nginx.conf /etc/nginx/sites-enabled/biztest' % env.project)
        sudo('service nginx reload')

    if not exists('%s/config.py' % env.project):
        sudo('cp %s/config-template %s/config.py' % (env.project, env.project))

    with virtualenv():
        run('pip install -r requirements.txt')

    if not exists('/root/bizness.db'):
        with virtualenv():
            run('PYTHONPATH=%s DATABASE_URL=sqlite:////root/bizness.db python %s/tools/populate_db.py' % (env.project, env.project))

    sudo('supervisorctl stop biztest')
    sudo('supervisorctl start biztest')

    #with cd(env.project):
    #    run('%s/node/bin/npm install' % env.root)
    #    run('%s/node/bin/bower install' % env.root)
    #    run('grunt')
