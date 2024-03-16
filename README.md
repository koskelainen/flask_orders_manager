## Running Docker

```shell
docker compose up -d
```

To access the application server, go to http://localhost:8180/

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
poetry run mamba tests/test_mamba/*.py
```

For running unittests with Docker postgresql, use the variable `DATABASE_URI_TEST` in the [.env.local](.env.local) and run:

```shell
poetry run python -m unittest discover -s tests/test_unittest
```

### Mamba coverage reports

For console report, run:

```shell

poetry run mamba tests/test_mamba/*.py --enable-coverage && poetry run coverage report -m  --rcfile=pyproject.toml
```

To generate an html report, run:

```shell
poetry run mamba tests/test_mamba/*.py --enable-coverage && poetry run coverage html -d coverage  --rcfile=pyproject.toml
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
