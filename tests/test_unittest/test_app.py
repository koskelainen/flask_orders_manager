from datetime import datetime
from urllib.parse import urljoin
from unittest.mock import Mock
import inject
from inject import clear as inject_clear
from flask import current_app, url_for
from flask_testing import TestCase

from src.adapter.models.models import OrderModel
from tests.conftest import clean, create_app, engine, session, set_up
from src.adapter.database.database import db

class MainTest(TestCase):
    def create_app(self):
        app = create_app()
        self.server_name = app.config.get("SERVER_NAME")
        return app

    def setUp(self):
        db.session = Mock(name="session")
        self.order_id = 1
        self.order_name = "Test Order"
        self.order_address = "Test Address"
        self.order_1 = OrderModel(id=1,
                                  name="Jon Snow",
                                  address="22781 Charles Shores Heathertown",
                                  created_at=datetime.now(),
                                  updated_at=datetime.now())
        self.order_2 = OrderModel(id=2,
                                  name="Timothy Jones",
                                  address="938 Bethany Course Suite 556 North Paul",
                                  created_at=datetime.now(),
                                  updated_at=datetime.now())

    def tearDown(self):
        # OrderModel.metadata.clear()
        inject_clear()

    @classmethod
    def setUpClass(cls):
        pass
        # set_up(test_engine=engine, test_session=session)

    @classmethod
    def tearDownClass(cls):
        # clean(test_engine=engine, test_session=session)
        inject_clear()

    def rebuild_response_location(self, response):
        _location = f"http://{self.server_name}"
        if response.location:
            _location = urljoin(f"http://{self.server_name}", response.location)
        response.location = _location
        return response

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config["TESTING"])

    def test_index_redirects(self):
        query = Mock(name="query")
        query.return_value = query
        db.session.query = query
        query.filter.return_value = query
        query.all.return_value = [self.order_2]
        response = self.client.get(url_for("index"))
        response = self.rebuild_response_location(response)
        self.assertRedirects(response, url_for("orders.order_list"))

    def test_get_orders_list(self):
        query = Mock(name="query")
        query.return_value = query
        db.session.query = query
        query.filter.return_value = query
        query.all.return_value = [self.order_1]
        response = self.client.get(url_for("orders.order_list"))
        self.assert200(response)

    def test_post_orders_list(self):
        response = self.client.post(url_for("orders.order_list"))
        self.assertTrue(response.status_code, 405)

    def test_orders_blueprint_exists(self):
        self.assertIn("orders", self.app.blueprints)

    def test_get_success_page(self):
        response = self.client.get(url_for("orders.success_page"))
        data = response.data.decode("utf-8")
        self.assert200(response)
        assert "Success" in data

    def test_get_failed_page(self):
        response = self.client.get(url_for("orders.failed_page"))
        data = response.data.decode("utf-8")
        self.assert200(response)
        assert "Failed" in data

    def test_template_order_list(self):
        query = Mock(name="query")
        query.return_value = query
        db.session.query = query
        query.all.return_value = [self.order_1, self.order_2]
        self.client.get(url_for("orders.order_list"))
        self.assertTemplateUsed("order_list.html")

    def test_template_create_list(self):
        db.session.query().filter_by(order_id=1).first.return_value = self.order_1
        self.client.get(url_for("orders.order_create"))
        self.assertTemplateUsed("order_create.html")

    def test_template_order_detail(self):
        db.session.query().filter_by(order_id=1).first.return_value = self.order_1
        self.client.get(url_for("orders.order_detail", order_id=1))
        self.assertTemplateUsed("order_detail.html")

    def test_template_order_update(self):
        db.session.query().filter_by(order_id=1).first.return_value = self.order_1
        self.client.get(url_for("orders.order_update", order_id=1))
        self.assertTemplateUsed("order_update.html")

    def test_template_order_delete(self):
        db.session.query().filter_by(order_id=1).first.return_value = self.order_1
        self.client.get(url_for("orders.order_delete", order_id=1))
        self.assertTemplateUsed("order_delete.html")

    def test_order_by_id(self):
        # For 200 Status
        order_id = 1
        db.session.query().filter_by(order_id=order_id).first.return_value = self.order_1
        response = self.client.get(f"/orders/{order_id}/detail")
        assert response.status_code == 200

        # For 404 Status
        order_id = 1234567
        db.session.query().filter_by(order_id=order_id).first.return_value = None
        response = self.client.get(f"/orders/{order_id}/detail")
        data = response.data.decode("utf-8")
        assert response.status_code == 404
        assert "Not Found" in data

    def test_post_order_create_success(self):
        form = {
            "name": "fake",
            "address": "fake-address",
        }

        response = self.client.post(url_for("orders.order_create"), data=form)
        response = self.rebuild_response_location(response)
        self.assertRedirects(response, url_for("orders.success_page"))

    def test_post_order_create_failed(self):
        form = {
            "name": "foo",
            "address": "12",
        }

        response = self.client.post(url_for("orders.order_create"), data=form)
        response = self.rebuild_response_location(response)
        self.assertRedirects(response, url_for("orders.failed_page"))

    def test_create_order(self):
        order = OrderModel(name=self.order_name, address=self.order_address)
        db.session.query().filter_by().first.return_value = order
        db.session.add.return_value = None
        db.session.commit.return_value = None
        db.session.add(order)
        db.session.commit()

        result = db.session.query(OrderModel).filter(OrderModel.name == self.order_name).first()  # NOQA
        self.assertIsNotNone(result)

    def test_update_order(self):
        order = OrderModel(name=self.order_name, address=self.order_address)
        db.session.query().filter_by().first.return_value = order
        db.session.add.return_value = None
        db.session.commit.return_value = None
        db.session.add(order)
        db.session.commit()

        order.name = updated_order = "Updated Order"
        db.session.commit()

        result = db.session.query(OrderModel).filter(OrderModel.name == updated_order).first()  # NOQA
        self.assertIsNotNone(result)
