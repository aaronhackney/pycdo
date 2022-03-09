from pycdo import CDOClient
from pycdo.model.tenants import TenantUser, TenantUserRole


def delete_test_user(cdo_client: CDOClient, user_name: str) -> None:
    """Delete the test user when needed"""
    user = cdo_client.search_tenant_username(user_name)
    if user:
        user = cdo_client.search_tenant_username(user_name)
        if user:
            cdo_client.delete_tenant_user(user[0].uid)


class TestCDOTenantUsers:
    def test_get_users(self, cdo_client: CDOClient):
        """Test getting all users for this tenant"""
        users = cdo_client.get_tenant_users()
        for user in users:
            assert user.uid

    def test_generate_token(self, cdo_api_user: TenantUser, cdo_client: CDOClient) -> None:
        """Given a tenant user (API-ONLY) generate a token for that user"""
        token = cdo_client.generate_tenant_user_api_token(cdo_api_user.name)
        assert token.access_token

    def test_revoke_token(self, cdo_api_user: TenantUser, cdo_client: CDOClient, test_user) -> None:
        """Test revoking an API token from an API-ONLY tenant user"""
        cdo_client.generate_tenant_user_api_token(cdo_api_user.name)
        user = cdo_client.search_tenant_username(test_user)
        cdo_client.revoke_tenant_user_api_token(user[0].api_token_id)
        user = cdo_client.search_tenant_username(test_user)
        assert user[0].api_token_id == None

    def test_create_api_user(self, cdo_client: CDOClient, test_user) -> None:
        """Test creating an API-ONLY tenant user"""
        user = cdo_client.add_tenant_user(test_user, "ROLE_READ_ONLY", is_api_user=True)
        assert user.uid
        delete_test_user(cdo_client, test_user)

    def test_create_user(self, cdo_client: CDOClient, test_user) -> None:
        """Test tenant user creation"""
        user = cdo_client.add_tenant_user(test_user, "ROLE_READ_ONLY")
        assert user.uid
        delete_test_user(cdo_client, test_user)

    def test_delete_user(self, cdo_client: CDOClient, test_user) -> None:
        """Test tenant user deletion"""
        user = cdo_client.add_tenant_user(f"{test_user}@test.pvt", "ROLE_READ_ONLY")
        assert user
        delete_test_user(cdo_client, test_user)
        users = cdo_client.search_tenant_username(test_user)
        assert not users

    def test_edit_user(self, cdo_client: CDOClient, cdo_user: TenantUser) -> None:
        """Test editing an existing user from this tenant"""
        cdo_user.roles = [TenantUserRole.read_only.value]
        cdo_client.update_tenant_user(cdo_user)
        assert cdo_client.search_tenant_username(cdo_user.name)[0].roles[0] == "ROLE_READ_ONLY"
