## Running Docker

```shell
docker compose up -d
```

To access the application server, go to http://localhost:8180/


## Using Makefile

To carry out operations, use the Makefile.

```
$ make help 
Please specify a build target. The choices are:
build                          Build all or c=<name> container
rebuild                        Stop containers (via 'down'), rebuilds services images (via 'build') and start services (via 'start')
up                             Start all or c=<name> containers in foreground
start                          Start all or c=<name> containers in background
stop                           Stop all or c=<name> containers
restart                        Restart all or c=<name> containers
logs                           Show logs for all or c=<name> containers
status                         Show status of containers
ps                             Alias of status
down                           Clean all data
clean                          Clean all data
install                        Install the poetry environment
check                          Run code quality tools.
flask                          Activate python and launch flask
ruffix                         Running ruff check --fix
test                           Test the code with mamba.
cov                            Coverage console mamba's tests
help                           Show help
```

## Running locally for development

### Setting up Poetry environment

This project utilizes Poetry for managing dependencies. To install dependencies, run:

```bash
poetry install
```

### Running the server

To run the server with gunicorn, use the following command:

```shell
gunicorn -w 2 -b 0.0.0.0:8080 --reload 'wsgi:app'
```

Alternatively, you can run the native Flask server with:

```shell
export FLASK_APP="wsgi:app"
flask run -h localhost -p 8000
```

### Running Tests

To run Mamba tests with mock and expects, use:

```shell
poetry run mamba tests/test_mamba/**/*.py
```

### Mamba coverage reports

For console report, run:

```shell

poetry run mamba tests/test_mamba/**/*.py --enable-coverage && poetry run coverage report -m  --rcfile=pyproject.toml
```

To generate an html report, run:

```shell
poetry run mamba tests/test_mamba/**/*.py --enable-coverage && poetry run coverage html -d coverage  --rcfile=pyproject.toml
```

<details>
<summary>
Unittest
</summary>


For running unittests with Docker postgresql, use the variable `DATABASE_URI_TEST` in the [.env.local](.env.local) and run:

```shell
poetry run python -m unittest discover -s tests/test_unittest
```

### Unittest coverage reports

For console report, run:

```shell
poetry run coverage run  --rcfile=pyproject.toml && poetry run coverage report -m  --rcfile=pyproject.toml
```

To generate an html report, run:

```shell
poetry run coverage run  --rcfile=pyproject.toml && poetry run coverage html -d coverage  --rcfile=pyproject.toml
```


</details>