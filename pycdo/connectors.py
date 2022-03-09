from pycdo.base import CDOBaseClient
from pycdo.model.connectors import Connector
import logging

logger = logging.getLogger(__name__)

# serviceConnectivityState
class CDOConnectors(CDOBaseClient):
    """Class for interacting with SDCs"""

    def get_sdc_list(self) -> Connector:
        """Get a list of SDCs in the tenant"""
        return [Connector(**proxy) for proxy in self.get_operation(self.PREFIX_LIST["CONNECTORS"])]
