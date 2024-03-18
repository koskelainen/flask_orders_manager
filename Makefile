ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

DOCKER_COMPOSE := docker-compose
DOCKER_COMPOSE_FILE := $(ROOT_DIR)/docker-compose.yml

VENV_NAME := .venv
VENV_PATH := ${ROOT_DIR}/${VENV_NAME}

.DEFAULT_GOAL := help

.PHONY: build
build: ## Build all or c=<name> container
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build $(c)

.PHONY: rebuild
rebuild: down build start## Stop containers (via 'down'), rebuilds services images (via 'build') and start services (via 'start')

.PHONY: up
up: ## Start all or c=<name> containers in foreground
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up $(c)

.PHONY: start
start: ## Start all or c=<name> containers in background
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d $(c)

.PHONY: stop
stop: ## Stop all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) stop $(c)

.PHONY: restart
restart: ## Restart all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) stop $(c)
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d $(c)

.PHONY: logs
logs: ## Show logs for all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs --tail=100 -f $(c)

.PHONY: status
status: ## Show status of containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) ps

.PHONY: ps
ps: status ## Alias of status

.PHONY: down
down: confirm ## Clean all data
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

.PHONY: clean
clean: confirm down ## Clean all data
	@rm -rf coverage
	@rm -f .coverage
	@find ./src -type d -name "__pycache__" | xargs rm -rf {};
	@find ./tests -type d -name "__pycache__" | xargs rm -rf {};

.PHONY: confirm
confirm:
	@echo "🚀 Clean temp data in project"
	@( read -p "$(RED)Are you sure? [y/N]$(RESET): " sure && case "$$sure" in [yY]) true;; *) false;; esac )

.PHONY: install
install: ## Install the poetry environment
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry env use 3.10
	@poetry install
	@poetry shell

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check"
	@poetry check --lock
	@echo "🚀 Linting with ruff"
	@poetry run ruff --config pyproject.toml

.PHONY: flask
flask: ## Activate python and launch flask
	@echo "🚀 Launch flask server"
	@export FLASK_APP="wsgi:app"
	@flask run -h localhost -p 8000

.PHONY: ruffix
ruffix: ## Running ruff check --fix
	@echo "🚀 Lint code: Running ruff check --fix"
	@poetry run ruff check --fix


.PHONY: test
test: ## Test the code with mamba.
	@echo "🚀 Testing code: Running mamba"
	@poetry run mamba tests/test_mamba/**/*.py


.PHONY: cov
cov: ## Coverage console mamba's tests
	@echo "🚀 Coverage code: Running mamba and coverage report in console"
	@poetry run mamba tests/test_mamba/**/*.py --enable-coverage
	@poetry run coverage report -m  --rcfile=pyproject.toml

.PHONY: help
help: ## Show help
	@echo Please specify a build target. The choices are:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
