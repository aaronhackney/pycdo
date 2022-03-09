from urllib import request
from pycdo.base import CDOBaseClient
from pycdo.model.tenants import Tenants, TenantUser, TenantContext, UserContext
from pycdo.model.token import Token
import logging
from typing import List
import json

log = logging.getLogger(__name__)


class CDOTenants(CDOBaseClient):
    """Class for performing CDO tenant operations"""

    def get_tenants(self) -> List[Tenants]:
        """
        Get a list of all CDO tenants in this region
        :return: list of tenants for which this user is entitled
        :rtype: list
        """
        test = self.get_operation(self.PREFIX_LIST["TENANTS"])
        return [Tenants(**tenant) for tenant in self.get_operation(self.PREFIX_LIST["TENANTS"])]

    def search_tenants(self, search_value: str) -> List[Tenants]:
        """
        Search tenant names (case insensitive) for the search value provided. Note will include substring matches!
        :param search_value: str to search for in tenant name
        :return: list of matches to the search value
        :rtype: list
        """
        matches = []
        tenants = self.get_tenants()
        if tenants:
            [matches.append(tenant) for tenant in tenants if (search_value.lower() in tenant.name.lower())]
        return matches

    def get_tenant_users(self) -> List[TenantUser]:
        """
        Returns a list of user objects for this tenant including name (email address), roles, apiTokenId and last login
        :return: list of user objects
        :rtype: list
        """
        test = self.get_operation(self.PREFIX_LIST["TENANT_USERS"])
        return [TenantUser(**user) for user in self.get_operation(self.PREFIX_LIST["TENANT_USERS"])]

    def search_tenant_username(self, username: str) -> List[TenantUser]:
        """Search for a username in a tenant and return the details if found.

        Args:
            username (str): username to search for in this tenant domain

        Returns:
            List[TenantUser]: list of TenantUser objects
        """
        users = [TenantUser(**user) for user in self.get_operation(self.PREFIX_LIST["TENANT_USERS"])]
        return [user for user in users if username in user.name]

    def get_tenant_context(self) -> List[TenantContext]:
        """
        Returns details of the tenant, including UID, EULA acceptance timestamp, auto deployment schedules, etc.
        :return: list of tenant details
        :rtype: list
        """
        return [TenantContext(**context) for context in self.get_operation(self.PREFIX_LIST["TENANT_CONTEXT"])]

    def add_tenant_user(self, username: str, role: str, is_api_user: bool = False) -> UserContext:
        """
        :param username:
        :param role: user role: [ROLE_READ_ONLY, ROLE_ADMIN, ROLE_SUPER_ADMIN]
        :param is_api_user: true if we are creating an API user
        :return:
        """
        data = {"roles": role, "isApiOnlyUser": True if is_api_user else False}
        return UserContext(**self.post_operation(f"{self.PREFIX_LIST['TENANT_USERS']}/{username}", data=data))

    def generate_tenant_user_api_token(self, username: str) -> Token:
        """
        Given the username in format username@account (API Only Accounts) generate an API token for that user
        :param username: an API only user in this tenant
        :return:
        """
        return Token(**self.post_operation(f"{self.PREFIX_LIST['TENANT_AUTH']}/token/{username}"))

    def revoke_tenant_user_api_token(self, api_token_id: str) -> Token:
        """
        Given the username in format username@account (API Only Accounts) generate an API token for that user
        :param username: an API only user in this tenant
        :return:
        """
        return self.post_operation(f"{self.PREFIX_LIST['TENANT_AUTH']}/revoke/{api_token_id}")

    def delete_tenant_user(self, uuid: str) -> None:
        """
        Given the uid of a user, delete the user from this tenant
        :param uuid: the user uid
        :type: str
        :return: None
        """
        self.delete_operation(f"{self.PREFIX_LIST['TENANT_USERS']}/{uuid}")

    def update_tenant_user(self, user: TenantUser):
        """
        :param TenantUser: TenantUser object with values we wish to update
        :return:
        """
        data = {"roles": user.roles, "isApiOnlyUser": True if user.is_api_only_user else False}
        return UserContext(**self.put_operation(f"{self.PREFIX_LIST['TENANT_USERS']}/{user.uid}", json=data))
