MANAGE := python django/hub/manage.py
UNAME_S := $(shell uname -s)
PYTEST_CMD := py.test django/hub  -s -x

GOOGLE_ID_DEV = ''
GOOGLE_KEY_DEV = ''

# Note that this ifeq-endif are space-indented for better readability
ifeq ($(UNAME_S), Linux)
    OPEN ?= xdg-open
endif
ifeq ($(UNAME_S), Darwin)
    OPEN ?= open
endif

env := development

# noop fallback
OPEN ?= :

app:
	cd django/hub/ && cookiecutter https://github.com/rpedigoni/cookiecutter-django-app

requirements:
	pip install -r django/requirements/$(env).txt

runserver:
	$(MANAGE) runserver --settings=settings.$(env)

syncdb:
	$(MANAGE) syncdb --all --noinput --settings=settings.$(env)

migrate:
	$(MANAGE) migrate --settings=settings.$(env)

conf-auth:
	$(MANAGE) set_google_oauth $(GOOGLE_ID_DEV) $(GOOGLE_KEY_DEV) --settings=settings.$(env)

test: clean
	$(PYTEST_CMD) --ds=settings.$(env)

coverage:
	$(PYTEST_CMD) --cov --ds=settings.$(env)

html:
	$(PYTEST_CMD) --cov --cov-report=html --ds=settings.$(env)
	$(OPEN) htmlcov/index.html

doc:
	$(MAKE) -C docs/ html
	$(OPEN) docs/build/html/index.html

deploy:
	fab -f django/fabfile.py deploy

clean:
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -rf docs/build/
	@pyclean .
	@echo "Cleaned."

SHELL = /bin/bash

install-dev: requirements syncdb conf-auth test
	@echo -e "\033[0;32m"
	@echo "Installed...."
	@echo "If you see this message all tests passed. Run application with: make runserver"
	@echo -e "\033[0m"

collectstatic:
	$(MANAGE) collectstatic --noinput

shell:
	$(MANAGE) shell --settings=settings.$(env)
