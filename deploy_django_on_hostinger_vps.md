# Django ML Model Deployment Guide - Hostinger KVM VPS

## Prerequisites

* Hostinger KVM VPS account

  * Use this link to purchase and get a discount: [Hostinger KVM VPS Discounted Link](https://hostinger.com?REFERRALCODE=1MUHAMMAD0984)
* Domain name (optional but recommended)

  * Buy a domain from [Namecheap](https://www.namecheap.com) or [GoDaddy](https://www.godaddy.com) or [Hostinger](https://www.hostinger.com)
* Local Django project ready for deployment

## Step 1: Server Setup and Initial Configuration

### 1.1 Connect to Your VPS using SSH

```bash
ssh root@your_vps_ip_address
```

You can see the following guide to use ssh via hostinger: [Hostinger SSH Guide](https://www.hostinger.com/support/5723772-how-to-connect-to-your-vps-via-ssh-at-hostinger/)

### 1.2 Update System Packages and Install Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y gcc python3-dev python3.12-venv nginx postgresql libpq-dev
```

## Step 2: Create Application User

### 2.1 Create Dedicated Django User

```bash
sudo useradd -m -s /bin/bash -G www-data django_user
sudo passwd django_user
sudo usermod -aG sudo django_user
sudo su - django_user
```

### 2.2 Set Directory Permissions

```bash
chmod 711 /home/django_user
cd /home/django_user
```

## Step 3: Setup PostgreSQL Database

### 3.1 Configure PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE ap_model_db;
CREATE USER ap_user WITH PASSWORD 'your_secure_password';
ALTER ROLE ap_user SET client_encoding TO 'utf8';
ALTER ROLE ap_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ap_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ap_model_db TO ap_user;
\c ap_model_db;
GRANT ALL PRIVILEGES ON SCHEMA public TO ap_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ap_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ap_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ap_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ap_user;
\q
```

## Step 4: Deploy Django Application

### 4.1 Clone Your Project

```bash
cd /home/django_user
git clone https://github.com/abid4850/Abid-Portfolio.git
```

### 4.2 Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4.3 Install Dependencies

```bash
pip install -r ./Abid-Portfolio/requirements.txt
pip install uwsgi psycopg2-binary
```

### 4.4 Setup Auto-activation

```bash
nano ~/.bashrc
```

Add:

```bash
cd
source .venv/bin/activate
```

### 4.5 Configure Django Settings for Production

```bash
cd ./Abid-Portfolio/abid_portfolio
nano settings_prod.py
```

```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ap_model_db',
        'USER': 'ap_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = '/home/django_user/Abid-Portfolio/abid_portfolio/staticfiles'
MEDIA_ROOT = '/home/django_user/Abid-Portfolio/abid_portfolio/media'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 4.6 Run Migrations & Collect Static Files

```bash
cd ~/Abid-Portfolio
export DJANGO_SETTINGS_MODULE=abid_portfolio.settings_prod
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

## Step 5: Configure uWSGI

### 5.1 Create uWSGI Configuration

```bash
nano /home/django_user/uwsgi.ini
```

```ini
[uwsgi]
chdir = /home/django_user/Abid-Portfolio/abid_portfolio
module = abid_portfolio.wsgi:application
home = /home/django_user/.venv
env = DJANGO_SETTINGS_MODULE=abid_portfolio.settings_prod
master = true
processes = 2
threads = 2
socket = /home/django_user/uwsgi.sock
chmod-socket = 660
chown-socket = django_user:www-data
vacuum = true
die-on-term = true
daemonize = /home/django_user/abid_portfolio.log
pidfile = /home/django_user/abid_portfolio.pid
```

### 5.2 Test uWSGI

```bash
uwsgi --ini /home/django_user/uwsgi.ini
ls -l /home/django_user/uwsgi.sock
tail -n60 /home/django_user/abid_portfolio.log
```

## Step 6: Configure Nginx

### 6.1 Create Nginx Configuration

```bash
sudo nano /etc/nginx/conf.d/Abid-Portfolio.conf
```

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate     /etc/ssl/certs/ip-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/ip-selfsigned.key;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/django_user/uwsgi.sock;
    }

    location /static/ {
        alias /home/django_user/Abid-Portfolio/abid_portfolio/staticfiles/;
    }

    location /media/ {
        alias /home/django_user/Abid-Portfolio/abid_portfolio/media/;
    }
}
```

### 6.2 Test and Start Nginx

```bash
sudo nginx -t
sudo systemctl restart nginx
```

## Step 7: SSL Certificate Setup

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Step 8: Final Testing

```bash
curl -I http://127.0.0.1
curl -I http://yourdomain.com
```

## Step 9: Maintenance & Updates

```bash
# Update code and dependencies
cd /home/django_user/Abid-Portfolio
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
uwsgi --reload /home/django_user/abid_portfolio.pid
```

## Auto SSL Renewal

```bash
sudo crontab -e
0 12 * * * /usr/bin/certbot renew --quiet && systemctl reload nginx
```

## Auto-update Django App Cron

```bash
nano ~/update_app.sh
chmod +x ~/update_app.sh
crontab -e
0 2 * * * /home/django_user/update_app.sh
```

# The End.





# Professional Update Workflow for portfolio.abidnexus.com

## 1. Git Version Control

* Commit and push all changes to your repository.
* Use feature branches for new updates:

```bash
git checkout -b feature/contact-form
# make changes
git commit -am "Added contact form"
git push origin feature/contact-form
```

* Merge into `main` after testing.

## 2. Local Testing Before Deployment

* Set up a local development environment matching production.
* Test locally:

```bash
python manage.py runserver
python manage.py test
python manage.py migrate --dry-run
```

* Collect static files:

```bash
python manage.py collectstatic --clear --noinput
```

## 3. Deployment Script (Automation)

* Pull latest code, install dependencies, migrate database, collect static files, reload uWSGI:

```bash
cd ~/Abid-Portfolio
git pull origin main
source ~/.venv/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=abid_portfolio.settings_prod
python manage.py migrate
python manage.py collectstatic --noinput
uwsgi --reload /home/django_user/abid_portfolio.pid
```

## 4. Zero-Downtime Updates

* Reload uWSGI gracefully:

```bash
uwsgi --reload /home/django_user/abid_portfolio.pid
```

* Avoid `uwsgi --stop` unless necessary.
* Keep a database backup:

```bash
pg_dump -U ap_user ap_model_db > ~/ap_model_db_backup.sql
```

## 5. Separate Production and Development Settings

* Use `settings_prod.py` for production and `settings_dev.py` for development.
* Keep sensitive info in environment variables:

```bash
export DATABASE_PASSWORD='yourpassword'
export SECRET_KEY='yoursecretkey'
```

## 6. Logging and Monitoring

* Monitor logs:

```bash
tail -f /home/django_user/abid_portfolio.log
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

* Optional: setup alerts with Prometheus/Grafana or cron emails.

## 7. Regular Backups

* Database backup:

```bash
pg_dump -U ap_user ap_model_db > ~/backup/ap_model_db_$(date +%F).sql
```

* Backup media/static files:

```bash
rsync -av ~/Abid-Portfolio/abid_portfolio/media/ ~/backup/media/
```

## 8. Staging Environment (Advanced)

* Use a separate staging deployment (e.g., `staging.abidnexus.com`) to test big updates.
* Merge to production only after testing.

## 9. Optional: Docker Deployment

* Containerize Django, PostgreSQL, and Nginx using Docker for consistent environment and easy rollback.

## Summary Professional Update Workflow

1. Develop on feature branch → push to Git
2. Test locally
3. Backup database + media
4. Pull updates on server (`git pull`)
5. Install new dependencies
6. Run migrations (`python manage.py migrate`)
7. Collect static files (`collectstatic`)
8. Reload uWSGI gracefully (`uwsgi --reload`)
9. Monitor logs
10. Rollback if needed (restore backup)

---

*Tip:* I can create a fully automated `update_app.sh` script for you, so updating your site becomes a single safe com
