# Basic Flask App
Simple flask application :)

### Steps to run app in developer mode:
In folder with Makefile run commands:<br>
`make venv` which creates virtualenv and install all required dependencies<br>
`make dev_run` which runs app locally ("localhost:5000/")

### Working with Heroku:
Firstly install heroku cli and create account: [Heroku DOC](https://devcenter.heroku.com/articles/getting-started-with-python)<br>

##### Commands to deploy:
1. `heroku create` only if it's new app, omit this step if you want just update.
2. `git push heroku master` or if you want push changes from another branch to test run: `git push heroku <branch>:master`.

##### Commands to check app:
1. `heroku open` or `heroku open --app <app_name>` opens application in web browser.
2. `heroku list` shows list of your apps.
3. `heroku logs --tail` shows logs.
