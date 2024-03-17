from unittest.mock import Mock, patch

import inject
from expects import equal, expect
from mamba import after, before, context, description, it

from src.application.order import Order
from src.domain.models import BaseOrderModel
from tests.conftest import create_app

with description("Test the core logic application by") as self:
    with context("launching it and verifying that"):
        with before.all:
            self.app = create_app()
            self.store = Order()
            self.mock_response = Mock()
            self.order = BaseOrderModel(name='Test Order', address='Test Address')

        with after.all:
            inject.clear()

        with it("check used method get_order"):
            with patch.object(Order, 'get_order', return_value=self.mock_response) as mock_method:
                response = self.store.get_order(order_id=1)
                mock_method.assert_called_once_with(order_id=1)
                expect(response).to(equal(self.mock_response))

        with it("check used method create_order"):
            with patch.object(Order, 'create_order', return_value=None) as mock_method:
                self.store.create_order(order=self.order)
                mock_method.assert_called_once_with(order=self.order)

        with it("check used method delete_order"):
            with patch.object(Order, 'delete_order', return_value=None) as mock_method:
                self.store.delete_order(order=self.order)
                mock_method.assert_called_once_with(order=self.order)

        with it("check used method update_order"):
            with patch.object(Order, 'update_order', return_value=self.mock_response) as mock_method:
                response = self.store.update_order(order=self.order)
                mock_method.assert_called_once_with(order=self.order)
                expect(response).to(equal(self.mock_response))
