py = /usr/bin/env python3
vpy = .venv/bin/python3
vpip = .venv/bin/pip3
req = requirements.txt
manage = manage.py
port = 8100
env = ./.env
setenv = set -a && source $(env) && set +a

init-deps:
	$(py) -m venv .venv
	@echo "Deps inited"
	@echo

install-deps:
	$(vpip) install -r $(req)
	@echo "Deps installed"
	@echo

migrate:
	@$(setenv) && $(vpy) $(manage) migrate
	@echo "Migrations applied"
	@echo

collect-static:
	@$(setenv) && $(vpy) $(manage) collectstatic --no-input

check-migrations:
	@$(setenv) && $(vpy) $(manage) makemigrations --check --dry-run
	@echo

test:
	@$(setenv) && $(vpy) $(manage) test -v 3
	@echo

runserver:
	@$(setenv) && $(vpy) $(manage) runserver $(port)

_shell:
	@$(setenv) && $(vpy) $(manage) shell

start: init-deps install-deps migrate collect-static runserver

up: check-migrations collect-static runserver

shell: check-migrations _shell
