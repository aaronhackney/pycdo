from pycdo import CDOClient


class TestCDODevices:
    """Test the CDO client tenant operations.
    Tests assume that a valid identity token will be found in the env variable CDO_TOKEN
    """

    def test_get_devices(self, cdo_client: CDOClient):
        devices = cdo_client.get_devices()
        for device in devices:
            assert device.uid is not None

    def test_get_devices_search(self, cdo_client: CDOClient):
        all_devices = cdo_client.get_devices()
        matched_devices = cdo_client.get_devices(search=all_devices[0].name)
        assert matched_devices

    def test_get_ftd_devices(self, cdo_client: CDOClient):
        all_devices = cdo_client.get_devices()
        for device in all_devices:
            if device.device_type == "FTD":
                device_obj = cdo_client.get_ftd_device(device.uid)
                assert device_obj.uid

    def test_get_asa_devices(self, cdo_client: CDOClient):
        all_devices = cdo_client.get_devices()
        for device in all_devices:
            if device.device_type == "ASA":
                device_obj = cdo_client.get_asa_device(device.uid)
                assert device_obj.uid
