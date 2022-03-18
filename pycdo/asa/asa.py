from pycdo.base import CDOBaseClient
from pycdo.model.asa.asa import ASA
import logging

logger = logging.getLogger(__name__)


class CDOASA(CDOBaseClient):
    def get_asa(self, name: str) -> ASA:
        """This call removes the tedious tasks of matching up a CDO object to an ASA object and associated records

        Args:
            name (str): The name of the ASA object in CDO that we wish to retrieve

        Returns:
            ASA: ASA object that contains the linked, associated objects and UIDs
        """
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
                    return asa  # A unified object with all of the needed mappings
