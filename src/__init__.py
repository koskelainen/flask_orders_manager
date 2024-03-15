from flask import Flask, make_response, redirect

from src.adapter.blueprints.order_blueprint import create_order_blueprint
from src.adapter.config.config import configure_application, configure_inject
from src.adapter.database.database import db


def create_application() -> Flask:
    application = Flask(__name__)

    configure_application(application)
    configure_inject()

    db.init_app(application)

    application.register_blueprint(create_order_blueprint(), url_prefix="/orders")

    @application.route("/")
    def index():
        return make_response(redirect("/orders/"))

    return application
