import os
import logging
from pycdo import CDOClient
from pycdo.polling import Polling
from pycdo.model.connectors import Connector
from pycdo.errors import AddDeviceException, AddCredentialsException


logger = logging.getLogger(__name__)


class MyASAOnboard:
    """Class to onboard an ASA to CDO"""

    def __init__(self, cdo_token: str, cdo_region: str) -> None:
        """Instantiate the CDOClient and the onboarding variables"""

        self.cdo_client = CDOClient(cdo_token, cdo_region)
        self.connector: Connector = None
        self.asa_device = None

    def get_connector(self, connector_name: str) -> None:
        """Get the connector (SDC/Cloud Connector) used to commnuicate with the ASA"""

        connectors = self.cdo_client.get_sdc_list()
        for connector in connectors:
            if connector.name == connector_name:
                self.connector = connector
                logger.warning(f"Found Connector: {connector.name}")

    def add_asa_to_cdo(self, asa_name: str, asa_ip: str, asa_port: str) -> None:
        """Add the ASA record to CDO and make sure it is avaialble"""

        self.asa_device = self.cdo_client.onboard_asa(asa_name, asa_ip, self.connector, port=asa_port)

        poll = Polling()  # Make sure that the device exists in CDO before we proceed
        if poll.poll(self.cdo_client.is_device_exists, 5, 2000, self.asa_device.uid):
            logger.warning(f"Device id {self.asa_device.uid} successfully added to CDO")
        else:
            logger.error(f"There was an issue adding the device {asa_name} to CDO")
            raise AddDeviceException(asa_name, asa_ip, asa_port)

    def add_asa_credentials(self, asa_user: str, asa_password: str) -> None:
        """Add the admin credentials for the ASA after assuring the device record is an a ready state"""

        poll = Polling()  # Make sure that the device in CDO is in a ready state; it may take a few seconds.
        if poll.poll(self.cdo_client.is_state, 5, 2000, self.asa_device.uid):
            asa_device = self.cdo_client.get_device(self.asa_device.uid)
            result = self.cdo_client.set_credentials(asa_device.uid, asa_user, asa_password, self.connector)
            if result:
                logger.warning("Successfully added credentials for this ASA to the Connector.")
            else:
                logger.error(f"There may have been an error adding credentials for ASA {self.asa_device.name}")
                raise AddCredentialsException(self.asa_device.name, self.asa_device.host, self.asa_device.port)

        else:
            logger.error(f"Device {self.asa_device.name} was not found in the CDO database")


def main():
    # 1. Instantiate our onboarding class (And the CDOClient)
    onboard = MyASAOnboard(CDO_TOKEN, CDO_REGION)

    # 2. Get the SDC or Cloud SDC/Gateway
    onboard.get_connector(CONNECTOR_NAME)

    # 3. Create the ASA object in CDO
    onboard.add_asa_to_cdo(ASA_NAME, ASA_IP, ASA_PORT)

    # 4. Add the ASA credentials to complete the ASA onboarding process
    onboard.add_asa_credentials(ASA_USER, ASA_PASS)


if __name__ == "__main__":
    # From environment variables
    CDO_TOKEN = os.environ.get("CDO_TOKEN")
    CDO_REGION = os.environ.get("CDO_REGION")

    # TODO: make these run time parameters
    ASA_USER = os.environ.get("ASA_USER")
    ASA_PASS = os.environ.get("ASA_PASS")
    ASA_IP = os.environ.get("ASA_IP")
    ASA_NAME = os.environ.get("ASA_NAME")
    ASA_PORT = os.environ.get("ASA_PORT")
    CONNECTOR_NAME = os.environ.get("CONNECTOR_NAME")

    main()  # Run the main loop of the program
