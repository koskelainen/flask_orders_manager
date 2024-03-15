from typing import List, Optional

from src.adapter.database.database import db
from src.adapter.models.models import OrderModel
from src.domain.order_orm import OrdersBasicORM


class OrdersORM(OrdersBasicORM):

    def __init__(self) -> None:
        super().__init__()

    def create_order(self, order: OrderModel) -> None:
        db.session.add(order)
        db.session.commit()

    def get_order(self, order_id: int) -> OrderModel | None:
        return db.session.query(OrderModel).filter_by(id=order_id).first()

    def update_order(self, order: OrderModel) -> OrderModel | None:
        result = db.session.query(OrderModel).filter_by(id=order.id).update(
            {OrderModel.name: order.name, OrderModel.address: order.address},
        )
        db.session.commit()
        return result

    def delete_order(self, order: OrderModel) -> None:
        obj = db.session.query(OrderModel).filter_by(id=order.id).first()
        db.session.delete(obj)
        db.session.commit()

    def search_orders(self, start_id: Optional[int] = None, end_id: Optional[int] = None) -> List[OrderModel]:
        query = db.session.query(OrderModel)
        if start_id:
            query = query.filter(OrderModel.id >= start_id)
        if end_id:
            query = query.filter(OrderModel.id <= end_id)
        return query.all()
