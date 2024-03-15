import inject
from flask_testing import TestCase

from src.adapter.constants.constants import NAME_MAX_LENGTH, NAME_MIN_LENGTH, ADDRESS_MAX_LENGTH, ADDRESS_MIN_LENGTH
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

    @staticmethod
    def _get_non_negative_length_plus_step(length, step=-1):
        _len = length + step
        if _len < 0:
            return 0
        return _len

    @staticmethod
    def get_dummy_order_form_data(order_data: dict) -> OrderForm:
        return OrderForm(DummyOrderData(order_data))

    def test_validate_success_order(self):
        form = self.get_dummy_order_form_data({"name": "example_name", "address": "example_address"})
        self.assertTrue(form.validate())

    def test_validate_invalid_order_small_name(self):
        form = self.get_dummy_order_form_data({
            "name": "".join(["a"] * self._get_non_negative_length_plus_step(NAME_MIN_LENGTH)),
            "address": "example_address",
        })
        self.assertFalse(form.validate())

    def test_validate_invalid_order_small_address(self):
        form = self.get_dummy_order_form_data({
            "name": "example_name",
            "address": "".join(["a"] * self._get_non_negative_length_plus_step(ADDRESS_MIN_LENGTH)),
        })
        self.assertFalse(form.validate())

    def test_validate_invalid_order_big_name(self):
        form = self.get_dummy_order_form_data({
            "name": "".join(["a"] * self._get_non_negative_length_plus_step(NAME_MAX_LENGTH, 1)),
            "address": "example_address",
        })
        self.assertFalse(form.validate())

    def test_validate_invalid_order_big_address(self):
        form = self.get_dummy_order_form_data({
            "name": "example_name",
            "address": "".join(["a"] * self._get_non_negative_length_plus_step(ADDRESS_MAX_LENGTH, 1)),
        })
        self.assertFalse(form.validate())

    def test_validate_invalid_order(self):
        form = self.get_dummy_order_form_data({
            "name": "".join(["a"] * self._get_non_negative_length_plus_step(NAME_MIN_LENGTH)),
            "address": "".join(["a"] * self._get_non_negative_length_plus_step(ADDRESS_MIN_LENGTH)),
        })
        self.assertFalse(form.validate())

    def test_validate_invalid_order_empty(self):
        form = self.get_dummy_order_form_data({"name": "", "address": ""})
        self.assertFalse(form.validate())

    def test_validate_invalid_order_empty_name(self):
        form = self.get_dummy_order_form_data({"name": "", "address": "example_address"})
        self.assertFalse(form.validate())

    def test_validate_invalid_order_empty_address(self):
        form = self.get_dummy_order_form_data({"name": "example_name", "address": ""})
        self.assertFalse(form.validate())
