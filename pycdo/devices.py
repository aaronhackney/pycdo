from pycdo.base import CDOBaseClient
from pycdo.model.devices import ASADevice, Device, FTDDevice
from requests import HTTPError
from typing import List
import logging

logger = logging.getLogger(__name__)


class CDODevices(CDOBaseClient):
    """Class for performing actions on devices in a CDO tenant"""

    def get_devices(self, search="") -> List[Device]:
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
        for device in self.get_operation(self.PREFIX_LIST["DEVICES"], params=params):
            devices.append(Device(**device))
        return devices

    def get_device(self, device_uid: str):
        """Given a device ID, retrieve the device data from CDO and attempt to return the correct object type.

        Args:
            device_uid (str): uid of the device to retrieve

        Returns:
            obj: Either returns the specific data type for the device retrieved or a dictionary
        """
        device = self.get_operation(f"{self.PREFIX_LIST['DEVICE']}/{device_uid}/specific-device")
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

    def get_asa_device(self, device_uid: str) -> ASADevice:
        """Given an ASA device uid, return the full details of the ASA device

        Args:
            device_uid (str): uid of the device to retrieve

        Returns:
            Device: ASADevice object containing the CDO device record and details
        """
        return ASADevice(**self.get_operation(f"{self.PREFIX_LIST['DEVICE']}/{device_uid}/specific-device"))

    def get_asa_device_configs(self, device_uid: str) -> ASADevice:
        """Given an ASA device uid, return the full details of the ASA device

        Args:
            device_uid (str): uid of the device to retrieve

        Returns:
            Device: ASADevice object containing the CDO device record and details
        """
        params = {"q": f"source.uid:{device_uid}"}
        return self.get_operation(f"{self.PREFIX_LIST['DEVICES-CONFIGS']}", params=params)

    def is_device_exists(self, device_uid: str) -> bool:
        """Try to retrieve a device by uid. If it exists, return true, if not, catch error and return false"""
        try:
            self.get_asa_device(device_uid)
            return True
        except HTTPError as ex:
            return False

    def is_state(self, device_uid: str, expected_state: str = "DONE"):
        """_summary_

        Args:
            cdo_client (CDOClient): CDOClient instance
            device_uid (str): The device uid for which we want to retrieve state
            expected_state (str, optional): The state we wish to check for. Defaults to "DONE".
        """
        test_device = self.get_device(device_uid)
        if test_device.state == expected_state:
            return True
        else:
            logger.warning(f"Device's expected state {expected_state} not found!")
            return False
