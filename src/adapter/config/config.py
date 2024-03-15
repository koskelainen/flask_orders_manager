from os import getenv

import inject
from flask import Flask

from src.adapter.database.order_orm import OrdersORM
from src.adapter.models.models import OrderModel
from src.domain.models import BaseOrderModel
from src.domain.order_orm import OrdersBasicORM


def make_dsn_url(
        driver: str = "postgresql+psycopg2",
        hostname: str = None,
        port: str = None,
        database_name: str = None,
        username: str = None,
        password: str = None,
) -> str:
    """
    Create a database URL to connect.
    :param driver: driver name like postgresql+psycopg2
    :param hostname: hostname
    :param port: port
    :param database_name: database_name
    :param username: username
    :param password: password
    :return: database URL to connect
    """
    hostname = hostname or getenv("POSTGRES_HOST", "localhost")
    port = port or getenv("POSTGRES_PORT", "5432")
    database_name = database_name or getenv("POSTGRES_DB", "postgres")
    username = username or getenv("POSTGRES_USER")
    password = password or getenv("POSTGRES_PASSWORD")
    return f"{driver}://{username}:{password}@{hostname}:{port}/{database_name}"


def configure_application(application: Flask) -> None:
    application.config.update(
        DATABASE_URI=getenv("DATABASE_URI", make_dsn_url()),
        SQLALCHEMY_DATABASE_URI=getenv("DATABASE_URI", make_dsn_url()),
    )
    # For CSRF token
    application.config["SECRET_KEY"] = getenv(
        "FLASK_SECRET_KEY",
        default="This key is top secret for us. Please don't share it to anyone.",
    )


def configure_inject() -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(OrdersBasicORM, OrdersORM())
        binder.bind(BaseOrderModel, OrderModel())

    inject.configure(config)
