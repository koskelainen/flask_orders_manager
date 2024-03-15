import inject
from expects import expect, be_true, be_false
from mamba import before, after, description
from mamba import it

from src.adapter.forms.forms import OrderForm
from tests.conftest import DummyOrderData

with description('Testing form validation') as self:
    with before.each:
        self.order_id = 1
        self.order_name = "Test Order"
        self.order_address = "Test Address"

    with after.each:
        inject.clear()

    with it('the successful validation of the normal order'):
        data = DummyOrderData({"name": "example_name", "address": "example_address"})
        form = OrderForm(data)
        expect(form.validate()).to(be_true)

    with it('Validate invalid order with the small name'):
        data = DummyOrderData({"name": "ex", "address": "example_address"})
        form = OrderForm(data)
        expect(form.validate()).to(be_false)

    with it('Validate invalid order with the small address'):
        data = DummyOrderData({"name": "example_name", "address": "ex"})
        form = OrderForm(data)
        expect(form.validate()).to(be_false)

    with it('Validate invalid order with the big name'):
        data = DummyOrderData({"name": "".join(["example_name"] * 30), "address": "example_address"})
        form = OrderForm(data)
        expect(form.validate()).to(be_false)

    with it('Validate invalid order with the big address'):
        data = DummyOrderData({"name": "example_name", "address": "".join(["example_address"] * 30)})
        form = OrderForm(data)
        expect(form.validate()).to(be_false)

    with it('Validate invalid order'):
        data = DummyOrderData({"name": "ex", "address": "ex"})
        form = OrderForm(data)
        expect(form.validate()).to(be_false)

    with it('Validate empty order'):
        data = DummyOrderData({"name": "", "address": ""})
        form = OrderForm(data)
        expect(form.validate()).to(be_false)

    with it('Validate invalid order without name'):
        data = DummyOrderData({"name": "", "address": "example_address"})
        form = OrderForm(data)
        expect(form.validate()).to(be_false)

    with it('Validate invalid order without address'):
        data = DummyOrderData({"name": "example_name", "address": ""})
        form = OrderForm(data)
        expect(form.validate()).to(be_false)
