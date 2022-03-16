__version__ = "0.1.5"

import logging

from pycdo.tenants import CDOTenants
from pycdo.base import CDOBaseClient
from pycdo.devices import CDODevices
from pycdo.changelogs import CDOChangeLogs
from pycdo.state_machine import CDOStateMachines
from pycdo.objects import CDOObjects
from pycdo.connectors import CDOConnectors
from pycdo.onboard import CDOOnboard

log = logging.getLogger(__name__)


class CDOClient(CDOTenants, CDODevices, CDOChangeLogs, CDOStateMachines, CDOObjects, CDOConnectors, CDOOnboard):
    """
    This package brings provides API access to Cisco Defense Orchestrator (CDO)
    """

    def __init__(self, api_token: str, region: str, api_version: str = "1", verify: str = ""):
        """This is the main client init process that controls all operations within CDO

        Args:
            api_token (str): _description_
            region (str): Endpoint FQDN e.g. "defenseorchestrator.com" "apj.cdo.cisco.com" "defenseorchestrator.eu"
            api_version (str, optional): For future use. Defaults to "1".
            verify (str, optional): For suture use for the  custom CA certificate use-case. Defaults to "".
        """
        CDOBaseClient.__init__(self, api_token, region, api_version=api_version, verify=verify)
