from pycdo.base import CDOBaseClient
from pycdo.model.devices import ASADevice, Device, FTDDevice, DeviceConfig, WorkingSet
from requests import HTTPError
from typing import List
import logging

from pycdo.model.objects import ObjectType

logger = logging.getLogger(__name__)

# TODO move device specific calls to device libs
class CDODevices(CDOBaseClient):
    """Class for performing actions on devices in a CDO tenant"""

    def get_target_devices(self, search="") -> List[Device]:
        """Get a summary of all devices in the CDO tenant

        Args:
            search (str, optional):  Optional return devices that have a name, IP address, or interface that matches
            our search string. Defaults to "".

        Returns:
            List[Devices]: List of "Devices" object types
        """
        if search:
            params = {"q": f"(name:*{search}*) OR (ipv4:*{search}*) OR (serial:*{search}*) OR (interfaces:*{search}*)"}
        else:
            params = None
        devices = []
        for device in self.get_operation(self.PREFIX_LIST["TARGET_DEVICES"], params=params):
            devices.append(Device(**device))
        return devices

    def get_device(self, device_uid: str):
        """Given a device ID, retrieve the device data from CDO and attempt to return the correct object type.

        Args:
            device_uid (str): uid of the device to retrieve

        Returns:
            obj: Either returns the specific data type for the device retrieved or a dictionary
        """
        return self.identify_device(self.get_operation(f"{self.PREFIX_LIST['DEVICE']}/{device_uid}/specific-device"))

    def get_asa_device_config_map(self, device_uid: str) -> dict:
        # TODO: return a data model
        """This maps the CDO object to an ASA device record. The relations flow goes:
           Target_Device --> Device_Config --> Config

        Args:
            device_uid (str): uid of the device to retrieve

        Returns:
            Device: ASADevice object containing the CDO device record and details
        """
        params = {"q": f"source.uid:{device_uid}"}
        result = self.get_operation(f"{self.PREFIX_LIST['ASA_DEVICES_CONFIGS']}", params=params)
        if result:
            return DeviceConfig(**result[0])

    def get_asa_config_obj(
        self,
        device_uid: str,
        resolve: str = (
            "[asa/configs.{name,namespace,type,version,state,stateDate,tags,tagKeys,tagValues,asaInterfaces,"
            "cryptoChecksum,selectedInterfaceObject,selectedInterfaceIP,securityContextMode,metadata}]"
        ),
    ) -> ASADevice:
        """This returns the ASA config object. The relations flow goes:
           Target_Device --> Device_Config --> Config

        Args:
            device_uid (str): uid of the device to retrieve (From the DeviceConfig object)
            resolve (str): The fields to reutrn from the query

        Returns:
            ASADevice: ASADevice object containing the CDO device record and details"""
        params = {"q": f"uid:{device_uid}", "resolve": resolve}
        result = self.get_operation(f"{self.PREFIX_LIST['ASA_CONFIGS']}", params=params)
        if result:
            return ASADevice(**result[0])

    def identify_device(self, device):
        """Given a devie object, attempt to returned a specific device type (ASA, FTD, etc)

        Args:
            device (dict): Device object

        Returns:
            ASADevice or FTDDevice: Return a device object or the original dict if no datatype is found
        """
        if device["namespace"] == "asa":
            return ASADevice(**device)
        elif device["namespace"] == "firepower":
            return FTDDevice(**device)
        else:
            return device

    def get_ftd_device(self, device_uid: str) -> FTDDevice:
        """Given an FTD device uid, return the full details of the FTD device

        Args:
            device_uid (str): uid of the device to retrieve

        Returns:
            Device: FTDDevice object containing the CDO device record and details
        """
        return FTDDevice(**self.get_operation(f"{self.PREFIX_LIST['DEVICE']}/{device_uid}/specific-device"))

    def get_workingset(self, target_uid):
        """Get the working set for operations like access-policies

        Args:
            target_uid (str): The CDO target object UID

        Returns:
            WorkingSet: workingset object
        """
        post_data = {
            "selectedModelObjects": [{"modelClassKey": "targets/devices", "uuids": [target_uid]}],
            "workingSetFilterAttributes": [],
        }
        return WorkingSet(**self.post_operation(f"{self.PREFIX_LIST['WORKINGSET']}", json=post_data))

    def is_device_exists(self, device_uid: str) -> bool:
        """Try to retrieve a device by uid. If it exists, return true, if not, catch error and return false

        Args:
            device_uid (str): uid of the device we are searching for

        Returns:
            bool: If the device exists, return true, if not, catch error and return false
        """
        try:
            self.get_device(device_uid)
            return True
        except HTTPError as ex:
            return False

    def is_state(self, device_uid: str, expected_state: str = "DONE") -> bool:
        """Check to see if the device is in the state we expect it to be.

        Args:
            cdo_client (CDOClient): CDOClient instance
            device_uid (str): The device uid for which we want to retrieve state
            expected_state (str, optional): The state we wish to check for. Defaults to "DONE".
        Returns:
            bool: return True if the expected_state == the actual state, else false
        """
        test_device = self.get_device(device_uid)
        if test_device.state == expected_state:
            return True
        else:
            logger.warning(f"Device's expected state {expected_state} not found!")
            return False
