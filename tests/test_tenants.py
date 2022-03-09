from pycdo import CDOClient


class TestCDOTenants:
    """Test the CDO client tenant operations"""

    def test_get_tenants(self, cdo_client: CDOClient) -> None:
        """Test getting a list of all tenants for the provided CDO token"""
        tenant_list = cdo_client.get_tenants()
        for tenant in tenant_list:
            assert tenant.uid is not None

    def test_search_tenants(self, cdo_client: CDOClient, search_tenant: str) -> None:
        """Test searching all tenants by name"""
        matched_tenants = cdo_client.search_tenants(search_tenant)
        assert matched_tenants

    def test_search_tenants_no_match(self, cdo_client: CDOClient):
        results = cdo_client.search_tenants("d1$")
        assert not results

    def test_get_tenant_context(self, cdo_client: CDOClient) -> None:
        """Test getting a tenant's context"""
        tenant_contexts = cdo_client.get_tenant_context()
        for tenant_context in tenant_contexts:
            assert tenant_context.uid
