FROM python:3.10-slim AS builder-base

ENV \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  PYSETUP_PATH="/opt/pysetup" \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # dockerize:
  USE_DOCKER=1 \
  DOCKERIZE_VERSION=v0.6.1 \
  # poetry:
  POETRY_VERSION=1.7.1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=false \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  # PostgreSQL Client major version
  PG_MAJOR_VERSION=13 \
  # account settings and common environment variables
  NB_USER=web \
  NB_UID=1000 \
  NB_PREFIX="/" \
  HOME="/home/$NB_USER" \
  SHELL=/bin/bash

# create user and set required ownership
RUN useradd -M -s /bin/bash -N -u ${NB_UID} ${NB_USER} \
 && mkdir -p ${HOME} \
 && chown -R ${NB_USER}:users ${HOME} \
 && chown -R ${NB_USER}:users /usr/local/bin

ARG PYTHON_VERSION=3.10.13
ARG PIP_VERSION=23.3.1

RUN pip install --upgrade pip==${PIP_VERSION}

# System deps:
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python3 -m venv ${POETRY_HOME} &&\
    ${POETRY_HOME}/bin/pip install poetry==${POETRY_VERSION}

WORKDIR $PYSETUP_PATH
COPY --chown=${NB_USER}:users pyproject.toml ./

FROM builder-base as prod

RUN poetry install --only=main --no-root --no-ansi

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR /app

RUN chown -R ${NB_USER}:users ${POETRY_HOME} \
    && rm -rf ${PYSETUP_PATH} \
    && rm -rf ${POETRY_CACHE_DIR}

USER ${NB_USER}

FROM builder-base as dev

ENV APP_ENV=dev
RUN poetry install $(test "$APP_ENV" == prod && echo "--only=main --no-root --no-ansi")

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR /app

RUN chown -R ${NB_USER}:users ${POETRY_HOME} \
    && rm -rf ${PYSETUP_PATH} \
    && rm -rf ${POETRY_CACHE_DIR}

USER ${NB_USER}

FROM builder-base as initdb

RUN poetry install --with initdb --no-root --no-ansi

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR /app

RUN chown -R ${NB_USER}:users ${POETRY_HOME} \
    && rm -rf ${PYSETUP_PATH} \
    && rm -rf ${POETRY_CACHE_DIR}

USER ${NB_USER}
