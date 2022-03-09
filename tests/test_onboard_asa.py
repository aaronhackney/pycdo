from pycdo import CDOClient
from requests.exceptions import HTTPError
from pycdo.polling import Polling
import os


class TestOnboardingASA:
    # DELETE /aegis/rest/v1/services/targets/devices/{device uid}}
    # TODO: Move test device details to environment variables
    ASA_NAME = "pytest-asav-1"
    ASA_IP = "172.30.4.101"
    ASA_PORT = "8443"
    ASA_USER = os.environ.get("ASA_USER")
    ASA_PASS = os.environ.get("ASA_PASS")
    # SDC = "demo-red-SDC-bxlab"
    # SDC = "Cloud Connector"
    SDC = "CDO_cisco_aahackne-SDC-1"

    def test_set_asa_credentials(self, cdo_client: CDOClient):
        sdcs = cdo_client.get_sdc_list()
        sdc = [sdc for sdc in sdcs if sdc.name == self.SDC][0]

        device = cdo_client.get_devices(search=self.ASA_NAME)[0]

        credentialed_asa = None
        poll = Polling()
        if poll.poll(cdo_client.is_state(device.uid)):
            asa_device = cdo_client.get_device(device.uid)
            credentialed_asa = cdo_client.set_credentials(asa_device.uid, self.ASA_USER, self.ASA_PASS, sdc)
        assert credentialed_asa

    def test_onboard_asa(self, cdo_client: CDOClient):
        sdcs = cdo_client.get_sdc_list()
        sdc = [sdc for sdc in sdcs if sdc.name == self.SDC][0]

        # Create the ASA object in CDO
        new_device = None
        try:
            new_device = cdo_client.onboard_asa(self.ASA_NAME, self.ASA_IP, sdc, port=self.ASA_PORT)
        except HTTPError as ex:
            if ex.response.status_code == 400:
                print("ERROR: Does this device/host/IP already exist in CDO?")
        assert new_device
