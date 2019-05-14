# virtualenv and run application
dev_run:
	. venv/bin/activate && gunicorn --chdir app main:app --bind 127.0.0.1:5000

venv:
	virtualenv -p /usr/bin/python3 venv/ && make venv_install_reqs && make venv_install_reqs_dev

venv_install_reqs:
	. venv/bin/activate && pip install -r requirements.txt

venv_install_reqs_dev:
	. venv/bin/activate && pip install -r requirements_dev.txt

# tests and maintaining code
bandit:
	. venv/bin/activate && bandit -r app/*.py

black_all:
	. venv/bin/activate && black -l 119 -S app/ unittests/

test-unittests:
	. venv/bin/activate && \
	export PYTHONPATH=$PYTHONPATH:app/ && \
	python -m pytest app/ unittests/ -v -ra --cov --cov-report term-missing:skip-covered --cov-fail-under=75 --pylama && \
	rm -r ".coverage" ".pytest_cache" "app/__pycache__" "unittests/__pycache__"
