import inject
from flask import Blueprint, Response, abort, redirect, render_template, request, session, url_for
from werkzeug.exceptions import HTTPException

from src.adapter.database.order_orm import OrderModel
from src.adapter.forms.forms import OrderForm
from src.application.order import Order
from src.application.search_orders import SearchOrders


@inject.autoparams()
def create_order_blueprint(
        single_order: Order,
        search_orders: SearchOrders,
) -> Blueprint:
    orders_blueprint = Blueprint("orders", __name__)

    @orders_blueprint.route("/success")
    def success_page() -> str:
        return render_template("success.html")

    @orders_blueprint.route("/failed")
    def failed_page() -> str:
        return render_template("failed.html")

    @orders_blueprint.route("/create", methods=["GET", "POST"])
    def order_create() -> str | Response:
        form = OrderForm()
        if form.is_submitted():
            session["action"] = "create"
            session["name"] = form.name.data.strip()
            session["address"] = form.address.data.strip()
            if form.validate_on_submit():
                order = OrderModel()
                form.populate_obj(order)
                form.name.data = None
                form.address.data = None
                single_order.create_order(order)
                return redirect(url_for("orders.success_page"))
            else:
                return redirect(url_for("orders.failed_page"))

        return render_template("order_create.html", form=form)

    @orders_blueprint.route("/<int:order_id>/detail", methods=["GET"])
    def order_detail(order_id: int) -> str:
        msg = f"The {order_id=} does not exist."

        if order_id < 1:
            return abort(404, msg)

        order = single_order.get_order(order_id=order_id)

        if not order:
            return abort(404, msg)

        return render_template("order_detail.html", order=order)

    @orders_blueprint.route("/<int:order_id>/update", methods=["GET", "POST"])
    def order_update(order_id: int) -> str | Response:
        order = single_order.get_order(order_id=order_id)
        form = OrderForm(obj=order)

        if not order:
            return abort(404, f"The {order_id=} does not exist.")

        if form.is_submitted():
            session["name"] = form.name.data.strip()
            session["address"] = form.address.data.strip()

            if form.validate_on_submit():
                new_order = OrderModel()
                form.populate_obj(new_order)
                new_order.id = order_id
                single_order.update_order(order=new_order)
                return redirect(url_for("orders.order_detail", order_id=order_id))
        return render_template("order_update.html", order=order, form=form)

    @orders_blueprint.route("/<int:order_id>/delete", methods=["GET", "POST"])
    def order_delete(order_id: int) -> str | Response:
        order = single_order.get_order(order_id=order_id)
        form = OrderForm(obj=order)
        if not order:
            return abort(404, f"The {order_id=} does not exist.")

        if form.is_submitted():
            single_order.delete_order(order=order)
            session["action"] = "delete"
            session["name"] = order.name
            session["address"] = order.address
            return redirect(url_for("orders.success_page"))

        return render_template("order_delete.html", order=order, form=form)

    @orders_blueprint.route("/", methods=["GET"])
    def order_list() -> str:
        start_id = request.args.get("start_id", default=None, type=int)
        end_id = request.args.get("end_id", default=None, type=int)
        orders = search_orders.execute(start_id=start_id, end_id=end_id)
        return render_template("order_list.html", orders=orders)

    @orders_blueprint.app_errorhandler(404)
    def handle_404(error):
        return render_template("errors/404.html", error=error), 404

    @orders_blueprint.app_errorhandler(500)
    def handle_500(error):
        return render_template("errors/500.html", error=error), 500

    @orders_blueprint.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            return error
        return render_template("errors/500.html", error=error), 500

    return orders_blueprint
