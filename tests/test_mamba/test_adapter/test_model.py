from datetime import datetime
from unittest.mock import Mock
from urllib.parse import urljoin

import inject
from expects import contain, equal, expect
from flask import url_for
from mamba import after, before, context, description, it

from src.adapter.database.database import db
from src.adapter.models.models import OrderModel
from tests.conftest import create_app

with description("Test the Flask app by") as self:
    def rebuild_response_location(self, response):
        _location = f"http://{self.server_name}"
        if response.location:
            _location = urljoin(f"http://{self.server_name}", response.location)
        response.location = _location
        return response


    with context("launching it and verifying that"):
        with before.all:
            self.app = create_app()
            db.session = Mock(name="session")
            self.server_name = self.app.config.get("SERVER_NAME")
            self.client = self.app.test_client()
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

        with after.all:
            inject.clear()

        with it("GET request detail to the order by id which does not exist."):
            order_id = 1234567
            db.session.query().filter_by().first.return_value = None
            response = self.client.get(f"/orders/{order_id}/detail")
            data = response.data.decode("utf-8")
            expect(response.status_code).to(equal(404))
            expect(data).to(contain("Not Found"))

        with it("GET request detail to the order by id = 0 which does not exist."):
            order_id = 0
            db.session.query().filter_by().first.return_value = None
            response = self.client.get(f"/orders/{order_id}/detail")
            data = response.data.decode("utf-8")
            expect(response.status_code).to(equal(404))
            expect(data).to(contain("Not Found"))

        with it("GET request update to the order by id = 0 which does not exist."):
            order_id = 0
            db.session.query().filter_by().first.return_value = None
            response = self.client.get(f"/orders/{order_id}/update")
            data = response.data.decode("utf-8")
            expect(response.status_code).to(equal(404))
            expect(data).to(contain("Not Found"))

        with it("GET request delete to the order by id = 0 which does not exist."):
            order_id = 0
            db.session.query().filter_by().first.return_value = None
            response = self.client.get(f"/orders/{order_id}/delete")
            data = response.data.decode("utf-8")
            expect(response.status_code).to(equal(404))
            expect(data).to(contain("Not Found"))

        with context("redirecting to"):
            with before.all:
                self.valid_status_codes = [301, 302, 303, 305, 307]

            with it("POST request create with valid data to the 'success' page."):
                form = {
                    "name": "fake",
                    "address": "fake-address",
                }
                expected_location = urljoin(f"http://{self.server_name}", "/orders/success")
                db.session.add.return_value = None
                db.session.commit.return_value = None
                response = self.client.post(url_for("orders.order_create"), data=form)
                response = self.rebuild_response_location(response)
                expect(self.valid_status_codes).to(contain(response.status_code))
                expect(response.location).to(equal(expected_location))

            with it("POST request update with valid data to the 'success' page."):
                valid_status_codes = [200]
                order_id = 1
                expected_location = urljoin(f"http://{self.server_name}", f"/orders/{order_id}/update")
                db.session.query().filter_by().first.return_value = self.order_1
                db.session.query().filter_by().update.return_value = self.order_1
                db.session.commit.return_value = None

                response = self.client.post(f"/orders/{order_id}/update")
                response = self.rebuild_response_location(response)
                expect(response.status_code).to(equal(200))
                expect(response.request.base_url).to(equal(expected_location))

            with it("POST request delete with valid data to the 'success' page."):
                order_id = 1
                expected_location = urljoin(f"http://{self.server_name}", "/orders/success")
                db.session.query().filter_by().first.return_value = self.order_1
                db.session.delete.return_value = None
                db.session.commit.return_value = None

                response = self.client.post(f"/orders/{order_id}/delete")
                response = self.rebuild_response_location(response)
                expect(self.valid_status_codes).to(contain(response.status_code))
                expect(response.location).to(equal(expected_location))

        with it("GET request to the order list."):
            valid_status_codes = [200]
            query = Mock(name="query")
            query.return_value = query
            db.session.query = query
            query.all.return_value = [self.order_1, self.order_2]
            response = self.client.get(url_for("orders.order_list"))
            expect(valid_status_codes).to(contain(response.status_code))
            data = response.data.decode("utf-8")
            expect(data).to(contain(self.order_1.name))
            expect(data).to(contain(self.order_1.address))
            expect(data).to(contain(self.order_2.name))
            expect(data).to(contain(self.order_2.address))

        with it("GET request to the order list with arguments 'order_1' and 'order_2'."):
            valid_status_codes = [200]
            query = Mock(name="query")
            query.return_value = query
            db.session.query = query
            query.filter.return_value = query
            query.all.return_value = [self.order_2]
            response = self.client.get("/orders/?start_id=2&end_id=2")
            data = response.data.decode("utf-8")
            expect(valid_status_codes).to(equal(valid_status_codes))
            expect(data).to(contain(self.order_2.name))
            expect(data).to(contain(self.order_2.address))
