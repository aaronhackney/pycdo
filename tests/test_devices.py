import logging
import os

from pycdo import CDOClient
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


class TestCDODevices:
    """Test the CDO client tenant operations.
    Tests assume that a valid identity token will be found in the env variable CDO_TOKEN
    """

    def test_get_target_devices(self, cdo_client: CDOClient):
        devices = cdo_client.get_target_devices()
        for device in devices:
            assert device.uid is not None

    def test_get_device(self, cdo_client: CDOClient):
        """Test getting a specific device objects"""
        devices = cdo_client.get_target_devices()
        for device in devices:
            try:
                test = cdo_client.get_device(device.uid)
                assert test
            except HTTPError as ex:
                logger.warning(
                    (
                        f"Device {device.name} of type {device.device_type} was not found."
                        "Not every device type has a corresponding 'specific-device' record."
                        "For example: DUO_ADMIN_PANEL, GENERIC_SSH, and IOS"
                    )
                )

    def test_get_devices_search(self, cdo_client: CDOClient):
        all_devices = cdo_client.get_target_devices()
        matched_devices = cdo_client.get_target_devices(search=all_devices[0].name)
        assert matched_devices

    def test_is_device_exists(self, cdo_client: CDOClient):
        all_devices = cdo_client.get_target_devices()
        assert cdo_client.is_device_exists(all_devices[0].uid)

    def test_is_device_exists_fail(self, cdo_client: CDOClient):
        is_device_exists = cdo_client.is_device_exists("abc1234")
        assert not is_device_exists

    def test_get_ftd_devices(self, cdo_client: CDOClient):
        all_devices = cdo_client.get_target_devices()
        for device in all_devices:
            if device.device_type == "FTD":
                device_obj = cdo_client.get_ftd_device(device.uid)
                assert device_obj.uid

    def test_get_asa_devices(self, cdo_client: CDOClient):
        all_devices = cdo_client.get_target_devices()
        for device in all_devices:
            if device.device_type == "ASA":
                device_obj = cdo_client.get_device(device.uid)
                assert device_obj.uid

    def test_get_asa_config_objs(self, cdo_client: CDOClient):
        """There needs to be at least 1 ASA in the tenant for this test"""
        test_device = None
        all_devices = cdo_client.get_target_devices()
        for device in all_devices:
            if device.device_type == "ASA":
                test_device = device
                break
        if test_device:
            device_config = cdo_client.get_asa_device_config_map(test_device.uid)
            asa_config_obj = cdo_client.get_asa_config_obj(device_config.target["uid"])
            assert asa_config_obj
        else:
            assert False  # We need an ASA for the test

    def test_get_asa_workingset(self, cdo_client: CDOClient):
        asa = cdo_client.get_asa(os.environ.get("TEST_ASA_NAME"))
        workingset = cdo_client.get_workingset(asa.target_device.uid)
        assert workingset
