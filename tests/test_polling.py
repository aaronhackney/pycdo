from pycdo import CDOClient
from datetime import datetime
from requests.exceptions import HTTPError
from pycdo.polling import Polling
import time


class TestPolling:
    def foo(self, a, b, c):
        print(f"A: {a} B: {b} C: {c}")

    def test_poll_variables(self, cdo_client: CDOClient):
        poll = Polling()
        test = poll.poll(self.foo, 5, 2000, "a", "b", "c")

    def test_polling_service(self, cdo_client: CDOClient):
        poll = Polling()
        devices = cdo_client.get_target_devices()
        for device in devices:
            if device.device_type == "ASA":
                test_device_uid = device.uid
                break
        assert poll.poll(cdo_client.is_state, 5, 2000, test_device_uid)

    def test_polling_fail(self, cdo_client: CDOClient):
        poll = Polling()
        devices = cdo_client.get_target_devices()
        for device in devices:
            if device.device_type == "ASA":
                test_device_uid = device.uid
                break
        assert not poll.poll(cdo_client.is_state(test_device_uid, expected_state="BORKED"))
