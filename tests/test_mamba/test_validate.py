import inject
from expects import be_false, be_true, expect
from mamba import after, before, description, it, context

from src.adapter.constants.constants import NAME_MAX_LENGTH, NAME_MIN_LENGTH, ADDRESS_MAX_LENGTH, ADDRESS_MIN_LENGTH
from src.adapter.forms.forms import OrderForm
from tests.conftest import DummyOrderData, create_app

app = create_app()
app.app_context().push()

with description("Testing form validation") as self:
    with context('Launch OrderForm tests'):
        with before.each:
            self.order_id = 1
            self.order_name = "Test Order"
            self.order_address = "Test Address"

        with after.each:
            inject.clear()


        def get_dummy_order_form_data(self, order_data: dict) -> OrderForm:
            return OrderForm(DummyOrderData(order_data))


        def _get_non_negative_length_plus_step(self, length, step=-1):
            _len = length + step
            if _len < 0:
                return 0
            return _len


        with it("the successful validation of the normal order"):
            form = self.get_dummy_order_form_data({"name": "example_name", "address": "example_address"})
            expect(form.validate()).to(be_true)

        with it("Validate invalid order with the small name"):
            form = self.get_dummy_order_form_data({
                "name": "".join(["a"] * self._get_non_negative_length_plus_step(NAME_MIN_LENGTH)),
                "address": "example_address",
            })
            expect(form.validate()).to(be_false)

        with it("Validate invalid order with the small address"):
            form = self.get_dummy_order_form_data({
                "name": "example_name",
                "address": "".join(["a"] * self._get_non_negative_length_plus_step(ADDRESS_MIN_LENGTH)),
            })
            expect(form.validate()).to(be_false)

        with it("Validate invalid order with the big name"):
            form = self.get_dummy_order_form_data({
                "name": "".join(["a"] * self._get_non_negative_length_plus_step(NAME_MAX_LENGTH, 1)),
                "address": "example_address"
            })
            expect(form.validate()).to(be_false)

        with it("Validate invalid order with the big address"):
            form = self.get_dummy_order_form_data({
                "name": "example_name",
                "address": "".join(["a"] * self._get_non_negative_length_plus_step(ADDRESS_MAX_LENGTH, 1)),
            })
            expect(form.validate()).to(be_false)

        with it("Validate invalid order"):
            form = self.get_dummy_order_form_data({
                "name": "".join(["a"] * self._get_non_negative_length_plus_step(NAME_MIN_LENGTH)),
                "address": "".join(["a"] * self._get_non_negative_length_plus_step(ADDRESS_MIN_LENGTH)),
            })
            expect(form.validate()).to(be_false)

        with it("Validate empty order"):
            form = self.get_dummy_order_form_data({"name": "", "address": ""})
            expect(form.validate()).to(be_false)

        with it("Validate invalid order without name"):
            form = self.get_dummy_order_form_data({"name": "", "address": "example_address"})
            expect(form.validate()).to(be_false)

        with it("Validate invalid order without address"):
            form = self.get_dummy_order_form_data({"name": "example_name", "address": ""})
            expect(form.validate()).to(be_false)
