# MiTi server information

Postgresql, NGINX, uWSGI, & certbot were all installed normally via apt-get and CLIxChat was cloned into `/var/clixchat/CLIxChat`. 

### CLIxChat
CLIxChat is written in Python 3.5 and depends on django-mptt to provide dialog trees and telepot to handle communicating with Telegram's bot API. Those and all other relevant python packages are available to be installed from requirements.txt:

`$ pip install -r requirements.txt`

The database was initialized via:

`$ python manage.py migrate`

and an admin account was added:

`$ python manage.py createsuperuser`

All CLIxChat print statements are routed into uWSGI's temporary log at `/tmp/uwsgi.log` so that identifiable information is not captured. All other logs are located in `/var/log/clixchat`

### uWSGI

The uWSGI folder is located at `/var/uwsgi` and config file is located at `/etc/uwsgi/apps-enabled/clixchat.ini`
The Telegram API token was generated via Telegram's botfather and is inside the uWSGI config file's env paramter.

~~~~
[uwsgi]
plugins = python3
project = CLIxChat
base = /var/clixchat
env = TELEGRAM_KEY=<bot-token>
chdir = %(base)/%(project)
wsgi-file = clixchat/wsgi.py
master = true
processes = 5
socket = /var/uwsgi/clixchat.sock
chown-socket = www-data:www-data
chmod-socket = 660
vacuum = true
~~~~

uWSGI logs to `/tmp/uwsgi.log` and has a socket located at `/run/uwsgi/clixchat.sock`

### NGINX

The NGINX config file is located at `/etc/nginx/sites-enabled/clixchat` 

~~~~
server {

    # SSL configuration

    listen 443 ssl http2 default_server;
    listen [::]:443 ssl http2 default_server;
    include snippets/ssl-miti.tiss.edu.conf;
    include snippets/ssl-params.conf;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
    root /var/clixchat/CLIxChat;
                    }
    location / {
    include         uwsgi_params;
    uwsgi_pass      unix:/var/uwsgi/clixchat.sock;
     }

}
~~~~

and logs to `/var/log/nginx/`

### Certbot Certificates

Telegram communicates over HTTPS. Certbot provides signed ssl certificates so Telegram's API can just be pointed at https://<your-web-address\>/bot/ 

`$ curl -F "url=https://<your web address>/bot/" https://api.telegram.org/bot<bot token>/setWebhook`

Information about Telegram & CLIxChat's interactions can be found here:
https://api.telegram.org/bot<bot-token\>/getWebhookInfo

Additional methods (such as deleting a webhook) are detailed in Telegram's documentation:
https://core.telegram.org/bots/api#making-requests

Certbot's certificates expire after 90 days but should auto-renew. If auto-renewing fails, you can manually update it via:

`$ sudo certbot --nginx renew`

Certbot logs to: `/var/log/letsencrypt/letsencrypt.log`

### Administration

Once your webserver is running go to https://\<your-web-address\>/admin to add dialog or examine users/administrators.

To add dialog, go to https://miti.tiss.edu/admin/bot/element/ 
The very top level item should be the word 'start' so that telegram knows where to start, but other than that you can fill it in as per the guidance document:
https://docs.google.com/document/d/11tMOqDr2WuadfihNZKdARdzAB46wOjR15JAb9SUhLI4/edit

Interactions with the bot are recorded here:
https://miti.tiss.edu/admin/bot/interaction/

An anonymized list of users is here along with their most recent location in the dialog tree:
https://miti.tiss.edu/admin/bot/user/

Administrators and account permissions can accessed here:
https://miti.tiss.edu/admin/auth/user/

### Backup

Last of all, the server has a backup cron job that both exports data as csv files for analysis and as sql dumps in case a database restoration is needed.
These jobs are located at /var/clixchat/backup.sh and in cron.

To retrieve the csv files for analysis, run:

`$ scp user@103.36.84.150:/var/clixchat/backups/*.csv ~`
