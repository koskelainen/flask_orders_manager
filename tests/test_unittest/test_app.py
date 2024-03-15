from urllib.parse import urljoin

import inject
from flask import current_app, url_for
from flask_testing import TestCase

from src.adapter.models.models import OrderModel
from tests.conftest import clean, create_app, engine, session, set_up


class MainTest(TestCase):
    def create_app(self):
        app = create_app()
        self.server_name = app.config.get("SERVER_NAME")
        return app

    def setUp(self):
        self.order_id = 1
        self.order_name = "Test Order"
        self.order_address = "Test Address"

    def tearDown(self):
        OrderModel.metadata.clear()
        inject.clear()

    @classmethod
    def setUpClass(cls):
        set_up(test_engine=engine, test_session=session)

    @classmethod
    def tearDownClass(cls):
        clean(test_engine=engine, test_session=session)

    def rebuild_response_location(self, response):
        response.location = urljoin(f"http://{self.server_name}", response.location)
        return response

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config["TESTING"])

    def test_index_redirects(self):
        response = self.client.get(url_for("index"))
        response = self.rebuild_response_location(response)
        self.assertRedirects(response, url_for("orders.order_list"))

    def test_get_orders_list(self):
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
        self.client.get(url_for("orders.order_list"))
        self.assertTemplateUsed("order_list.html")

    def test_template_create_list(self):
        self.client.get(url_for("orders.order_create"))
        self.assertTemplateUsed("order_create.html")

    def test_template_order_detail(self):
        self.client.get(url_for("orders.order_detail", order_id=1))
        self.assertTemplateUsed("order_detail.html")

    def test_template_order_update(self):
        self.client.get(url_for("orders.order_update", order_id=1))
        self.assertTemplateUsed("order_update.html")

    def test_template_order_delete(self):
        self.client.get(url_for("orders.order_delete", order_id=1))
        self.assertTemplateUsed("order_delete.html")

    def test_order_by_id(self):
        # For 200 Status
        order_id = 1
        response = self.client.get(f"/orders/{order_id}/detail")
        data = response.data.decode("utf-8")
        assert response.status_code == 200
        assert self.order_name in data
        assert self.order_address in data

        # For 404 Status
        order_id = 1234567
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
        session.add(order)
        session.commit()

        result = session.query(OrderModel).filter(OrderModel.name == self.order_name).first()  # NOQA
        self.assertIsNotNone(result)

    def test_update_order(self):
        order = OrderModel(name=self.order_name, address=self.order_address)
        session.add(order)
        session.commit()

        order.name = updated_order = "Updated Order"
        session.commit()

        result = session.query(OrderModel).filter(OrderModel.name == updated_order).first()  # NOQA
        self.assertIsNotNone(result)
