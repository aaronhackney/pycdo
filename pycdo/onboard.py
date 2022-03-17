from pycdo.base import CDOBaseClient
from pycdo.model.devices import Device
from pycdo.model.connectors import Connector
from pycdo.encrypt import EncryptCredentials
import logging

logger = logging.getLogger(__name__)


class CDOOnboard(CDOBaseClient):
    """Class for onboarding devices into CDO"""

    def onboard_asa(
        self, name: str, host: str, connector: Connector, device_type: str = "ASA", port: int = 443
    ) -> Device:
        """Step 1 to onboard a device to CDO. (Does not set credentials. See set_credentials for that)

        Args:
            name (str): Name of the device in CDO
            host (str): IP address or hostname of the device we are onboarding
            connector (Connector): Cloud SDC/CDG or OnPrem SDC object
            device_type (str, optional): Type of device we are onboarding. Defaults to "ASA".
            port (int, optional): Port that the device's administrative interface listens on. Defaults to 443.

        Returns:
            Device: A Device object containing the data sent back by the onboard API call
        """
        if connector.cdg:
            lar_type = "CDG"  # Cloud gateway
            lar_uid = None
        else:
            lar_type = "SDC"  # OnPrem SDC
            lar_uid = connector.uid

        post_data = {
            "deviceType": device_type,
            "larUid": lar_uid,
            "larType": lar_type,
            "name": name,
            "host": host,
            "ipv4": f"{host}:{port}",
            "model": False,
            "metadata": {"isNewPolicyObjectModel": True},
        }
        onboarded_asa = Device(**self.post_operation(f"{self.PREFIX_LIST['TARGET_DEVICES']}", json=post_data))
        return onboarded_asa

    def set_credentials(self, device_uid: str, asa_user: str, asa_pass: str, sdc: Connector) -> dict:
        """Set the credentials for a recently onboarded ASA
        Args:
            device_uid (str): The UID of the device we want to set the credentials on
            asa_user (str): ASA username
            asa_pass (str): ASA password
            sdc (Connector): A cloud or onprem SDC

        Returns:
            dict: A dictionary containing the API response to the set creentials IP call
        """
        # TODO: Model the API repsonse
        return self.put_operation(
            f"{self.PREFIX_LIST['SERVICES']}/asa/configs/{device_uid}",
            json=self._generate_credential_payload(asa_user, asa_pass, sdc),
        )

    def _generate_credential_payload(self, asa_user: str, asa_pass: str, sdc: Connector) -> dict:
        """If we use a cloud sdc, generate a simple, clear-text payload. If we use an On-Prem SDC, encrypt as needed

        Args:
            asa_user (str): ASA username
            asa_pass (str): ASA password
            sdc (Connector): SDC object

        Returns:
            dict: A dictionary containing the needed elements
        """
        if sdc.cdg:  # CDGs accept clear text credentials
            return {
                "state": "CERT_VALIDATED",
                "credentials": f'{{"username":"{asa_user}","password":"{asa_pass}"}}',
            }
        else:  # SDCs require us to encrypt the credentials with the SDCs Public Key
            username = EncryptCredentials.encrypt(asa_user, sdc.lar_public_key.encoded_key)
            password = EncryptCredentials.encrypt(asa_pass, sdc.lar_public_key.encoded_key)
            key_id = sdc.lar_public_key.key_id
            return {
                "state": "CERT_VALIDATED",
                "credentials": (f'{{"keyId":"{key_id}",' f'"username":"{username}",' f'"password":"{password}"}}'),
            }
