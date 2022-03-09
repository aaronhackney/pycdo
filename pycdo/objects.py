from pytest import param
from pycdo import CDOBaseClient
from pycdo.model.objects import NetworkObject
import logging
from typing import List


log = logging.getLogger(__name__)


class CDOObjects(CDOBaseClient):
    """CRUD operations for CDO Objects"""

    def _build_query(self, kwargs: dict) -> dict:
        """Build the complex query for retreiving objects
        Args:
            kwargs:
                limit (int, optional): number of records to return at one time. Defaults to 100 (API MAX = 200)
                offset (int, optional): useful for paging records over multiple api calls. Defaults to 0.
                sort (str, optional): Order in which to sort the returned records. Defaults to "name:asc".
                object_type (str, optional): Type of object to return NETWORK
                device_type (str, optional): Type of device object applies to [ASA, FTD...]

        Returns:
            dict: dictionary of the query data for the object API call
        """
        query_parts = [
            "(cdoInternal:false) AND (isReadOnly:false OR metadata.CDO_FMC_READONLY:true OR objectType:SGT_GROUP)",
        ]
        query_parts.append(f"objectType:{kwargs['object_type']}") if "object_type" in kwargs else None
        query_parts.append(f"deviceType:{kwargs['device_type']}") if "device_type" in kwargs else None
        query_parts.append(f"issueType:{kwargs['issue_type']}") if "issue_type" in kwargs else None

        return {
            "q": " AND ".join(["(" + line + ")" for line in query_parts]),
            "limit": kwargs["limit"] if "limit" in kwargs else 100,
            "offset": kwargs["offset"] if "offset" in kwargs else 0,
            "sort": kwargs["sort"] if "sort" in kwargs else "name:asc",
        }

    def get_objects(self, **kwargs):
        """Return objects (Filterable)
        Args:
            kwargs:
                limit (int, optional): number of records to return at one time. Defaults to 100 (API MAX = 200)
                offset (int, optional): useful for paging records over multiple api calls. Defaults to 0.
                sort (str, optional): Order in which to sort the returned records. Defaults to "name:asc".
                object_type (str, optional): Type of object to return NETWORK
                device_type (str, optional): Type of device object applies to [ASA, FTD...]
                issue_type (str, optional): Filter on special cases [SHARED, ...]
        Returns:
            dict: dictionary of objects returned by the query string
        """
        objs_returned = self.get_operation(f"{self.PREFIX_LIST['OBJECTS']}", params=self._build_query(kwargs))
        cdo_objs = []
        for cdo_obj in objs_returned:
            if (
                cdo_obj["objectType"] == "NETWORK_OBJECT"
                or cdo_obj["objectType"] == "NETWORK_GROUP"
                or cdo_obj["objectType"] == "PROTOCOL_GROUP"
                or cdo_obj["objectType"] == "SERVICE_PROTOCOL_OBJECT"
            ):
                cdo_objs.append(NetworkObject(**cdo_obj))
            else:
                cdo_objs.append(cdo_obj)
        return cdo_objs
