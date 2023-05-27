Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* virtualenv + pip
* Git

eg, on Ubuntu:

    sudo apt upadate
    sudo apt install nginx git python3 python3-venv
    
## Nginx Virtual Host config

* see nginx.template.conf
* replace DOMAIN with, e.g., staging.my-domain.org

## Systemd service

* see gunicorn-systemd.template.service
* replace DOAMIN with e.g., staging.my-domain.org

## Folder structure:

Assume we have a user account at /home/username

/home/username
└── sites
    ├── DOMAIN1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    └── virtualenv
    └── DOMAIN2
         ├── .env
         ├── db.sqlite3
         ├── etc
         

