from pycdo.model.asa.asa import ASA
from pycdo.base import CDOBaseClient
from pycdo.model.devices import ASADevice, Device, FTDDevice, DeviceConfig
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
        # return [
        #     DeviceConfig(**device)
        #     for device in self.get_operation(f"{self.PREFIX_LIST['ASA_DEVICES_CONFIGS']}", params=params)
        # ]

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
            Device: ASADevice object containing the CDO device record and details"""
        params = {"q": f"uid:{device_uid}", "resolve": resolve}
        result = self.get_operation(f"{self.PREFIX_LIST['ASA_CONFIGS']}", params=params)
        if result:
            return ASADevice(**result[0])

    def get_asa(self, name: str = "") -> ASA:
        """This call removes the tedious tasks of matching up a CDO object to an ASA object and associated records."""
        asa = ASA(name=name)
        for device in self.get_target_devices(search=name):
            if device.name == name:
                asa.target_device = device  # Get the target device details
                if asa.target_device:
                    asa.device_config = self.get_asa_device_config_map(
                        asa.target_device.uid
                    )  # get the target-to-device mapping
                    asa.asa = self.get_asa_config_obj(
                        asa.device_config.target["uid"]
                    )  # Get the actual ASA object in CDO
                    return asa

    def identify_device(self, device):
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

    def get_working_set(self):
        """POST /aegis/rest/v1/services/common/workingset
        DATA=
        {"selectedModelObjects":[{"modelClassKey":"targets/devices","uuids":["511524f1-e76d-4597-9055-e0264a0d2442"]}],"workingSetFilterAttributes":[]}


        """

    def get_asa_access_groups(
        self,
        working_set: str,
        shared: bool = False,
        resolve: str = (
            "[targets/accessgroups.{@HEADER,editable,properties,issueTypes,issueDigest,deviceUid,deviceUids,"
            "asaInterfaces,shared}]"
        ),
        sort: str = "name",
        limit: int = 100,
        offset: int = 0,
    ):
        """_summary_

        Args:
            working_set (str): Working set UID returned by get_asa_workingset()
            shared (bool, optional): Defaults to False.
            resolve (str, optional): Proopertiers to retrieve
            sort (str, optional): Sort Order. Defaults to "name".
            limit (int, optional): used in paging. Defaults to 100.
            offset (int, optional): used in paging. Defaults to 0.

        Returns:
            _type_: _description_
        """
        params = {
            "q": f"shared:{shared}",
            "resolve": resolve,
            "sort": sort,
            "workingSet": working_set,
            "limit": limit,
            "offset": offset,
        }
        return self.get_operation(f"{self.PREFIX_LIST['ACCESS_GROUPS']}", params=params)

    def get_asa_access_policy(self, policy_uid):
        # TODO: Model access-list data access_list['namespace']=targets, access_list['type']=accessgroups
        """Get the access-list rules (ACEs) for the given access policy.

        Args:
            policy_uid (str): The UID of the access-group that is the parent of this policy
        """
        return self.get_operation(f"{self.PREFIX_LIST['ACCESS_POLICIES']}/{policy_uid}")

    def get_asa_workingset(self, target_uid):
        # TODO: Model working set data
        """Get the working set for operations like access-policies

        Args:
            target_uid (str): The CDO target object UID

        Returns:
            dict: type: workingset namespace: common
        """
        post_data = {
            "selectedModelObjects": [{"modelClassKey": "targets/devices", "uuids": [target_uid]}],
            "workingSetFilterAttributes": [],
        }

        return self.post_operation(f"{self.PREFIX_LIST['WORKINGSET']}", json=post_data)

    def is_device_exists(self, device_uid: str) -> bool:
        """Try to retrieve a device by uid. If it exists, return true, if not, catch error and return false"""
        try:
            self.get_device(device_uid)
            return True
        except HTTPError as ex:
            return False

    def is_state(self, device_uid: str, expected_state: str = "DONE") -> bool:
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
