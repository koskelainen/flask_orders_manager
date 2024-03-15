import inject
from flask_testing import TestCase

from src.adapter.forms.forms import OrderForm
from tests.conftest import DummyOrderData, create_app


class OrderFormTest(TestCase):
    def create_app(self):
        app = create_app()
        self.server_name = app.config.get("SERVER_NAME")
        return app

    def setUp(self):
        self.order_id = 1
        self.order_name = "Test Order"
        self.order_address = "Test Address"

    def tearDown(self):
        inject.clear()

    def test_validate_success_order(self):
        data = DummyOrderData({"name": "example_name", "address": "example_address"})
        form = OrderForm(data)
        self.assertTrue(form.validate())

    def test_validate_invalid_order_small_name(self):
        data = DummyOrderData({"name": "ex", "address": "example_address"})
        form = OrderForm(data)
        self.assertFalse(form.validate())

    def test_validate_invalid_order_small_address(self):
        data = DummyOrderData({"name": "example_name", "address": "ex"})
        form = OrderForm(data)
        self.assertFalse(form.validate())

    def test_validate_invalid_order_big_name(self):
        data = DummyOrderData({"name": "".join(["example_name"] * 30), "address": "example_address"})
        form = OrderForm(data)
        self.assertFalse(form.validate())

    def test_validate_invalid_order_big_address(self):
        data = DummyOrderData({"name": "example_name", "address": "".join(["example_address"] * 30)})
        form = OrderForm(data)
        self.assertFalse(form.validate())

    def test_validate_invalid_order(self):
        data = DummyOrderData({"name": "ex", "address": "ex"})
        form = OrderForm(data)
        self.assertFalse(form.validate())

    def test_validate_invalid_order_empty(self):
        data = DummyOrderData({"name": "", "address": ""})
        form = OrderForm(data)
        self.assertFalse(form.validate())

    def test_validate_invalid_order_empty_name(self):
        data = DummyOrderData({"name": "", "address": "example_address"})
        form = OrderForm(data)
        self.assertFalse(form.validate())

    def test_validate_invalid_order_empty_address(self):
        data = DummyOrderData({"name": "example_name", "address": ""})
        form = OrderForm(data)
        self.assertFalse(form.validate())
