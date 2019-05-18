# Book manager
Simple flask application :)

### Steps to run app in developer mode:
Firstly you need to prepare config_dev.py file in app/config:
```python
#!/usr/bin/env python3
"""Developer config."""
class APP:
    IP = "0.0.0.0"
    PORT = 12000
    SECRET_KEY = 'test123'
class DB:
    USER = 'books_manager'
    PASSWORD = 'postgres1'
    HOST = '0.0.0.0'
    PORT = 5432
    DBNAME = 'books_db'
```
In folder with Makefile run commands:<br>
`make venv` which creates virtualenv and install all required dependencies<br>
`make dev_run` which runs app locally ("localhost:5000/")

If you don't have installed postgres you can use docker-compose.yml in docker directory:
`docker-compose up -d`

When everything is working, you need to create table in database:
`source venv/bin/activate`
`python manage.py`


### Working with Heroku:
Firstly install heroku cli and create account: [Heroku DOC](https://devcenter.heroku.com/articles/getting-started-with-python)<br>

##### Commands to deploy:
1. `heroku create` only if it's new app, omit this step if you want just update.
2. `git push heroku master` or if you want push changes from another branch to test run: `git push heroku <branch>:master`.

##### Commands to check app:
1. `heroku open` or `heroku open --app <app_name>` opens application in web browser.
2. `heroku list` shows list of your apps.
3. `heroku logs --tail` shows logs.
