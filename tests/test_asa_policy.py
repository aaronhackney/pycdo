from pycdo import CDOClient


class TestASAPolicies:
    """Test ASA Policy Manipulation"""

    def test_get_access_groups(self, cdo_client: CDOClient):
        """ """
        # Get CDO device objects
        target_devices = cdo_client.get_target_devices()
        target_device_list = [item for item in target_devices if item.device_type == "ASA"]

        # Link a specific device to the CDO placeholder object
        device_config_obj_list = cdo_client.get_asa_device_config_map(target_device_list[0].uid)

        print()
