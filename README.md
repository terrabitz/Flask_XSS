# Flask XSS 

This is an intentionally vulnerable webapp designed to explore various XSS attacks against web
apps. It was created as a companion to the "Web Application Hacker's Handbook" chapter 12.

## Features
* GET parameter XSS
* Cookie-base XSS
* Stored XSS
* Hackable 'admin' user
* Toggleable browser XSS protection

## Installation
To install, just run the following:

```
git clone https://github.com/terrabitz/Flask_XSS
cd flask_xss
pip install -r requirements.txt
python manage.py db init 
python manage.py add_admin
python manage.py runserver
```

The development server should then be started on `localhost:5000`