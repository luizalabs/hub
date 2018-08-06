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
	$(MANAGE) runserver --settings=settings

syncdb:
	$(MANAGE) syncdb --all --noinput --settings=settings

migrate:
	$(MANAGE) migrate --settings=settings

conf-auth:
	$(MANAGE) set_google_oauth $(GOOGLE_ID_DEV) $(GOOGLE_KEY_DEV) --settings=settings

test: clean
	$(PYTEST_CMD) --ds=settings

coverage:
	$(PYTEST_CMD) --cov --ds=settings

html:
	$(PYTEST_CMD) --cov --cov-report=html --ds=settings
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
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@echo "Cleaned."

SHELL = /bin/bash

install-dev: requirements syncdb conf-auth test
	@echo -e "\033[0;32m"
	@echo "Installed...."
	@echo "If you see this message all tests passed. Run application with: make runserver"
	@echo -e "\033[0m"

collectstatic:
	@mkdir -p static
	$(MANAGE) collectstatic --noinput

shell:
	$(MANAGE) shell --settings=settings

preview-release:
	@towncrier --draft

release-patch:
	@bumpversion patch
	@towncrier --yes
	@git commit -am 'Update CHANGELOG'

release-minor:
	@bumpversion minor
	@towncrier --yes
	@git commit -am 'Update CHANGELOG'

release-major:
	@bumpversion major
	@towncrier --yes
	@git commit -am 'Update CHANGELOG'
