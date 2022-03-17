from pycdo.base import CDOBaseClient
from pycdo.model.asa.access_rule import AccessRule, AccessGroup
from typing import List
import logging

logger = logging.getLogger(__name__)


class CDOASAAccessPolicies(CDOBaseClient):
    """Class for CRUD operations for ASA AccessGroups/ACLs"""

    def get_asa_access_groups(
        self,
        working_set: str,
        shared: bool = False,
        resolve: str = (
            "[targets/accessgroups.{@HEADER,editable,properties,issueTypes,issueDigest,deviceUid,deviceUids,"
            "asaInterfaces,shared}]"
        ),
        sort: str = "name",
        limit: int = 100,
        offset: int = 0,
    ):
        """Get the list of AccessGroups/ACLS. Note we only have access to ACLs pinned to Access Groups on the ASA

        Args:
            working_set (str): Working set UID returned by get_asa_workingset()
            shared (bool, optional): Defaults to False.
            resolve (str, optional): Proopertiers to retrieve
            sort (str, optional): Sort Order. Defaults to "name".
            limit (int, optional): used in paging. Defaults to 100.
            offset (int, optional): used in paging. Defaults to 0.

        Returns:
            List[AccessGroup]: Returns a lsit of AccessGroup Objects
        """
        params = {
            "q": f"shared:{shared}",
            "resolve": resolve,
            "sort": sort,
            "workingSet": working_set,
            "limit": limit,
            "offset": offset,
        }
        return [
            AccessGroup(**item) for item in self.get_operation(f"{self.PREFIX_LIST['ACCESS_GROUPS']}", params=params)
        ]

    def get_asa_access_policy(self, policy_uid):
        """Get the access-list rules (ACEs) for the given access policy.

        Args:
            policy_uid (str): The UID of the access-group that is the parent of this policy
        """
        return AccessGroup(**self.get_operation(f"{self.PREFIX_LIST['ACCESS_GROUPS']}/{policy_uid}"))

    def update_access_policy(self, policy_uid: str, access_list: List[AccessRule]) -> AccessGroup:
        """Update the access-policy with all of the access-rules presented. This is also used to ADD new rules.

        Args:
            policy_uid (str): The access-group UID
            access_list (list[AccessRule]): AccessRules with which we will replace/update the policy

        Returns:
            AccessGroup: modified access-group/ACL object including list of ACEs
        """
        payload = {"accessRules": [ace.dict(by_alias=True) for ace in access_list]}
        return AccessGroup(**self.put_operation(f"{self.PREFIX_LIST['ACCESS_GROUPS']}/{policy_uid}", json=payload))
