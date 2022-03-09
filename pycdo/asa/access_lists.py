from pycdo.base import CDOBaseClient
from pycdo.model.change_logs import ChangeLog
from typing import List
import logging

logger = logging.getLogger(__name__)


class CDOASAAccessLists(CDOBaseClient):
    """Class for getting changelogs from a CDO tenant"""

    def get_all_access_lists(self):
        """Return all access-lists"""
