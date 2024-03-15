import inject

from src.domain.models import BaseOrderModel
from src.domain.order_orm import OrdersBasicORM


class Order:
    @inject.autoparams("database")
    def __init__(self, database: OrdersBasicORM):
        self.__database = database

    def get_order(self, order_id: int) -> BaseOrderModel:
        return self.__database.get_order(order_id)

    def create_order(self, order: BaseOrderModel) -> None:
        return self.__database.create_order(order)

    def delete_order(self, order: BaseOrderModel) -> None:
        return self.__database.delete_order(order)

    def update_order(self, order: BaseOrderModel) -> BaseOrderModel:
        return self.__database.update_order(order)
