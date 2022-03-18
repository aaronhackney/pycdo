from pycdo import CDOClient
import logging
import os

logger = logging.getLogger(__name__)


class TestCDOASA:
    def test_get_asa(self, cdo_client: CDOClient):
        asa = cdo_client.get_asa(os.environ.get("TEST_ASA_NAME"))
        assert asa.asa
