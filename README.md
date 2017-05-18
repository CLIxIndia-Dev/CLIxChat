# CLIxChat

CLIxChat is written in python 3.5

Install postgresql

Install the packages in requirements.txt

`pip install -r requirements.txt`

Update the database

`python manage.py migrate`

Setup the admin account

`python manage.py createsuperuser`

Telegram communicates over https. Get certs and register them and your api endpoint like so:

`curl -F "url=https://<your web address>/bot/" -F "certificate=/locationof/cert.crt" https://api.telegram.org/bot<your bot token>/setWebhook`

You'll also need to set the environment variable on your local computer: 

`export TELEGRAM_KEY=<your bot token>`

You can gunicorn for a webserver like this:

`gunicorn -b <your ip address> -w3 --certfile=server.crt --keyfile=server.key clixchat.wsgi`

but you should probably add nginx as you scale users.

Once your webserver is up though you can go to https://\<your web address\>/admin to start putting in content. You have to name the very top level item in 'Elements' the word 'start' so that telegram knows where to start, but other than that you can fill it in as desired.
