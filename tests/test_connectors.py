from pycdo import CDOClient
from datetime import datetime


class TestConnectors:
    def test_get_connectors(self, cdo_client: CDOClient):
        sdc_list = cdo_client.get_sdc_list()
        assert sdc_list
