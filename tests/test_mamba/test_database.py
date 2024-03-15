from datetime import datetime
from unittest.mock import Mock

import inject
from expects import expect, equal, be_none
from mamba import before, after, description
from mamba import it

from src.adapter.models.models import OrderModel
from src.application.order import Order
from src.application.search_orders import SearchOrders
from src.domain.order_orm import OrdersBasicORM

with description('Mocking ORM testing') as self:
    with before.each:
        self.store = Mock()
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
        self.injector(self.store)

    with after.each:
        inject.clear()


    def injector(self, database: Mock) -> None:
        inject.clear_and_configure(lambda binder: binder
                                   .bind(OrdersBasicORM, database))


    with it('create new order'):
        self.store.create_order.return_value = None
        result = Order().create_order(1)  # NOQA
        expect(result).to(be_none)
        expect(self.store.create_order.call_count).to(equal(1))

    with it('get stored order by id'):
        self.store.get_order.return_value = self.order_1
        result = Order().get_order(1)
        expect(result).to(equal(self.order_1))
        expect(self.store.get_order.call_count).to(equal(1))

    with it('update stored order by id'):
        self.store.get_order.return_value = self.order_1
        cur_order = Order().get_order(1)
        self.order_1.name = "Larry Vaughan"
        cur_order.name = "Larry Vaughan"
        self.store.update_order.return_value = self.order_1
        result = Order().update_order(cur_order)
        expect(result).to(equal(self.order_1))
        expect(self.store.update_order.call_count).to(equal(1))

    with it('delete stored order by id'):
        self.store.delete_order.return_value = None
        result = Order().delete_order(1)  # NOQA
        expect(result).to(be_none)
        expect(self.store.delete_order.call_count).to(equal(1))

    with it('search orders by start_id=1 and end_id=8'):
        self.store.search_orders.return_value = [self.order_1, self.order_2]
        result = SearchOrders().execute(start_id=1, end_id=8)
        expect(result).to(equal(([self.order_1, self.order_2])))
        expect(self.store.search_orders.call_count).to(equal(1))
        self.store.search_orders.assert_called_once_with(start_id=1, end_id=8)
