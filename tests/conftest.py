import os
import pytest
from pycdo import CDOClient
from pycdo.model.tenants import TenantUser

""" 
These unit tests require the following environment variables to be defined with working values:
CDO_TOKEN=[your cdo api token]
CDO_REGION=[us, eu, apj]
SEARCH_TENANT=[Some tenant name in your account]
"""


@pytest.fixture
def test_user():
    return "test-api-only"


@pytest.fixture
def search_tenant():
    return os.environ["SEARCH_TENANT"]


@pytest.fixture
def cdo_api_user(request, cdo_client: CDOClient, test_user, scope="module") -> TenantUser:
    """Create test user and delete when tests are finished"""
    cdo_client.add_tenant_user(test_user, "ROLE_SUPER_ADMIN", is_api_user=True)
    user = cdo_client.search_tenant_username(test_user)[0]

    def fin():
        user = cdo_client.search_tenant_username(test_user)
        if user:
            cdo_client.delete_tenant_user(user[0].uid)

    request.addfinalizer(fin)
    return user


@pytest.fixture
def cdo_user(request, cdo_client: CDOClient, test_user, scope="module") -> TenantUser:
    """Create test user and delete when tests are finished"""
    cdo_client.add_tenant_user(f"{test_user}@test.pvt", "ROLE_SUPER_ADMIN", is_api_user=False)
    user = cdo_client.search_tenant_username(test_user)[0]

    def fin():
        user = cdo_client.search_tenant_username(test_user)
        if user:
            cdo_client.delete_tenant_user(user[0].uid)

    request.addfinalizer(fin)
    return user


@pytest.fixture
def cdo_client(scope="module") -> CDOClient:
    """Get a CDO client for testing use"""
    return CDOClient(os.environ["CDO_TOKEN"], os.environ["CDO_REGION"])
