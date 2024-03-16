from os import environ, getenv
from pathlib import Path

from dotenv import load_dotenv
from inject import clear as inject_clear
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src import create_application
from src.adapter.models.models import OrderModel

ROOT_DIR = Path(__file__).resolve().parent.parent

for fpath in [ROOT_DIR.joinpath(".env"), ROOT_DIR.joinpath(".env.local")]:
    if fpath.exists():
        load_dotenv(dotenv_path=fpath, override=True)


def make_session_and_engine():
    engine = create_engine(getenv("DATABASE_URI_TEST"))
    _test_session = sessionmaker(bind=engine)
    session = _test_session()
    return engine, session


engine, session = make_session_and_engine()


def create_app():
    environ["DATABASE_URI"] = getenv("DATABASE_URI_TEST")
    environ["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI_TEST")

    application = create_application()

    application.config["TESTING"] = True
    application.config["DEBUG"] = True
    application.config["WTF_CSRF_ENABLED"] = False
    application.config["SERVER_NAME"] = application.config.get("SERVER_NAME") or "localhost"

    application.app_context().push()

    return application


def set_up(test_engine: Engine, test_session: Session):
    OrderModel.metadata.create_all(bind=test_engine)
    order = OrderModel(
        name="Test Order",
        address="Test Address",
    )
    test_session.add(order)
    test_session.commit()


def clean(test_engine: Engine, test_session: Session):
    OrderModel.metadata.drop_all(bind=test_engine)
    test_session.close()
    test_engine.dispose()
    inject_clear()


class DummyOrderData(dict):
    def getlist(self, key):
        v = self[key]
        if not isinstance(v, (list, tuple)):
            v = [v]
        return v
