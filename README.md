## Run Docker

```shell
docker compose up -d
```

Application server: http://localhost:8180/

## Run dev local

### Poetry env

Project working with Poetry

```bash
poetry install
```

### Run server

Run server with gunicorn
```shell
gunicorn -w 2 -b 0.0.0.0:8080 --reload 'wsgi:app'
```

Run native flask server

```shell
export FLASK_APP="wsgi:app"
flask run -h localhost -p 8000
```

### Tests

Run Mamba tests, with mock and expects
```shell
poetry run mamba tests/test_mamba/*.py
```

Run unittests, with Docker postgresql. File [.env.local](.env.local) variable - `DATABASE_URI_TEST` 

```shell
poetry run python -m unittest discover -s tests/test_unittest
```

### Coverage

Console report 

```shell
poetry run coverage run  --rcfile=pyproject.toml && poetry run coverage report -m  --rcfile=pyproject.toml
```

html report

```shell
poetry run coverage run  --rcfile=pyproject.toml && poetry run coverage html -d coverage  --rcfile=pyproject.toml
```