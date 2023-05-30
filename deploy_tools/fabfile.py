import random
from fabric import task

REPO_URL = 'https://github.com/stokeham/superlists.git'

@task
def deploy(c):
    site_folder = f'/home/{c.user}/sites/{c.host}'
    c.run(f'mkdir -p {site_folder}')
    print(f'created {site_folder}')
    with c.cd(site_folder):
        _get_latest_source(c)
        _update_virtualenv(c)
        _create_or_update_dotenv(c)
        _update_static_files(c)
        _update_database(c)

def _get_latest_source(c):
    if c.run('test -d .git', warn=True):
        print('has .git directory, running git fetch')
        c.run('git fetch')
        print('fetched')
    else:
        print(f'no git directory - going to clone from {REPO_URL}')
        c.run(f'git clone {REPO_URL} .')
    r = c.run("git log -n 1 --format=%H")
    print(f'reseting against: {r.stdout}')
    c.run(f'git reset --hard {r.stdout}')

def _update_virtualenv(c):
    if c.run('test -f virtualenv/bin/pip',warn=True).failed:
        c.run(f'python3 -m venv virtualenv')
    c.run('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv(c):
    if c.run('test -f .env', warn=True).failed:
        c.run('touch .env')
    current_contents = c.run('cat .env')
    if 'DJANGO_DEBUG_FALSE' not in current_contents.stdout:
        c.run('echo DJANGO_DEBUG_FALSE=y >> .env')
    if 'SITENAME' not in current_contents.stdout:
        c.run(f'echo SITENAME={c.host} >> .env')
    if 'DJANGO_SECRET_KEY' not in current_contents.stdout:
        new_secret = ''.join(random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50))
        c.run(f'echo DJANGO_SECRET_KEY={new_secret} >> .env')

def _update_static_files(c):
    c.run('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database(c):
    c.run('./virtualenv/bin/python manage.py migrate --noinput')
