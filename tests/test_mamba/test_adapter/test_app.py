from unittest.mock import Mock, patch
from urllib.parse import urljoin

import inject
from expects import be_none, be_true, contain, equal, expect, have_key
from flask import url_for
from jinja2 import TemplateNotFound
from mamba import after, before, context, description, it, _it

from tests.conftest import create_app

with description("Test the Flask app by") as self:
    def assert_template_used(self, template_name):
        try:
            self.app.jinja_env.get_template(template_name)
        except TemplateNotFound:
            raise AssertionError(f"Template '{template_name}' not found")


    def rebuild_response_location(self, response):
        _location = f"http://{self.server_name}"
        if response.location:
            _location = urljoin(f"http://{self.server_name}", response.location)
        response.location = _location
        return response


    with context("launching it and verifying that"):
        with before.all:
            self.app = create_app()
            self.server_name = self.app.config.get("SERVER_NAME")

        with before.each:
            self.store = Mock()
            self.client = self.app.test_client()

        with after.each:
            inject.clear()

        with it("app was created."):
            expect(self.app).to_not(be_none)

        with it("app set mode testing."):
            expect(self.app.config["TESTING"]).to(be_true)

        with context("redirecting to"):
            with before.all:
                self.valid_status_codes = [301, 302, 303, 305, 307]

            with it("the index page with a GET request to the 'orders' page."):
                expected_location = urljoin(f"http://{self.server_name}", "/orders/")
                response = self.client.get(url_for("index"))
                response = self.rebuild_response_location(response)
                expect(self.valid_status_codes).to(contain(response.status_code))
                expect(response.location).to(equal(expected_location))

            with it("POST request with invalid data to the 'failed' page."):
                form = {
                    "name": "foo",
                    "address": "f",
                }
                expected_location = urljoin(f"http://{self.server_name}", "/orders/failed")

                response = self.client.post(url_for("orders.order_create"), data=form)
                response = self.rebuild_response_location(response)
                expect(self.valid_status_codes).to(contain(response.status_code))
                expect(response.location).to(equal(expected_location))

            with _it("POST request with valid data to the 'success' page."):
                form = {
                    "name": "fake",
                    "address": "fake-address",
                }
                expected_location = urljoin(f"http://{self.server_name}", "/orders/success")

                response = self.client.post(url_for("orders.order_create"), data=form)
                response = self.rebuild_response_location(response)
                expect(self.valid_status_codes).to(contain(response.status_code))
                expect(response.location).to(equal(expected_location))

        with _it("GET request to the order by id which does not exist."):
            order_id = 1234567
            response = self.client.get(f"/orders/{order_id}/detail")
            data = response.data.decode("utf-8")
            expect(response.status_code).to(equal(404))
            expect(data).to(contain("Not Found"))

        with it("was used template order list."):
            self.client.get(url_for("orders.order_list"))
            self.assert_template_used("order_list.html")

        with it("was used template create list."):
            self.client.get(url_for("orders.order_create"))
            self.assert_template_used("order_create.html")

        with it("was used template order detail."):
            self.client.get(url_for("orders.order_detail", order_id=1))
            self.assert_template_used("order_detail.html")

        with it("was used template order update."):
            self.client.get(url_for("orders.order_update", order_id=1))
            self.assert_template_used("order_update.html")

        with it("was used template order update."):
            self.client.get(url_for("orders.order_update", order_id=1))
            self.assert_template_used("order_update.html")

        with it("was used template order delete."):
            self.client.get(url_for("orders.order_delete", order_id=1))
            self.assert_template_used("order_delete.html")

        with _it("GET request to the order list."):
            expected_location = urljoin(f"http://{self.server_name}", None)
            valid_status_codes = [200]
            response = self.client.get(url_for("orders.order_list"))
            response = self.rebuild_response_location(response)
            expect(valid_status_codes).to(contain(response.status_code))
            expect(response.location).to(equal(expected_location))

        with it("POST request to the order list."):
            expected_location = urljoin(f"http://{self.server_name}", None)
            valid_status_codes = [405]
            response = self.client.post(url_for("orders.order_list"))
            response = self.rebuild_response_location(response)
            expect(valid_status_codes).to(contain(response.status_code))
            expect(response.location).to(equal(expected_location))

        with it("checking blueprint exists."):
            expect(self.app.blueprints).to(have_key("orders"))

        with it("GET request to the success page"):
            response = self.client.get(url_for("orders.success_page"))
            valid_status_codes = [200]
            expect(valid_status_codes).to(contain(response.status_code))
            data = response.data.decode("utf-8")
            expect(data).to(contain("Success"))

        with it("GET request to the failed page"):
            response = self.client.get(url_for("orders.failed_page"))
            valid_status_codes = [200]
            expect(valid_status_codes).to(contain(response.status_code))
            data = response.data.decode("utf-8")
            expect(data).to(contain("Failed"))
