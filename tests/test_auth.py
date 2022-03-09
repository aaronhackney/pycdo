from pycdo import CDOClient
from requests import HTTPError


class TestCDOAuth:
    """Test CDO Token auth"""

    def test_get_with_valid_api_key(self, cdo_client: CDOClient):
        tenants = cdo_client.get_tenants()
        for tenant in tenants:
            assert tenant.uid
        assert tenants

    def test_get_with_bad_api_key(self, cdo_client: CDOClient):
        cdo_client.http_session.headers["Authorization"] = "Bearer abc1234567890"
        tenants = None
        try:
            tenants = cdo_client.get_tenants()
        except HTTPError as err:
            assert err.response.status_code == 401
        assert tenants is None
