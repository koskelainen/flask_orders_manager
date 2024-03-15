from typing import Optional

import inject

from src.domain.models import BaseOrderModel
from src.domain.order_orm import OrdersBasicORM


class SearchOrders:
    @inject.autoparams("database")
    def __init__(self, database: OrdersBasicORM):
        self.__database = database

    def execute(self, start_id: Optional[int], end_id: Optional[int]) -> list[BaseOrderModel]:
        return self.__database.search_orders(start_id=start_id, end_id=end_id)
