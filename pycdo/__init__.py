__version__ = "0.1.5"

import logging

from pycdo.tenants import CDOTenants
from pycdo.base import CDOBaseClient
from pycdo.devices import CDODevices
from pycdo.changelogs import CDOChangeLogs
from pycdo.state_machine import CDOStateMachines
from pycdo.mssp import CDOMSSPClient
from pycdo.objects import CDOObjects
from pycdo.connectors import CDOConnectors
from pycdo.onboard import CDOOnboard

log = logging.getLogger(__name__)


class CDOClient(
    CDOTenants, CDODevices, CDOChangeLogs, CDOStateMachines, CDOMSSPClient, CDOObjects, CDOConnectors, CDOOnboard
):
    """
    This package brings provides API access to Cisco Defense Orchestrator (CDO)
    """

    def __init__(self, api_token, region, api_version="1", verify=""):
        CDOBaseClient.__init__(self, api_token, region, api_version=api_version, verify=verify)
