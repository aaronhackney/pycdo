from pycdo import CDOClient


class TestCDOObjects:
    """Test CDOObject operations"""

    def test_get_all_network_objects(self, cdo_client: CDOClient) -> None:
        all_net_objs = cdo_client.get_objects(object_type="*NETWORK*")
        assert all_net_objs

    def test_get_network_objects(self, cdo_client: CDOClient) -> None:
        net_objs = cdo_client.get_objects(object_type="NETWORK_OBJECT")
        assert net_objs

    def test_get_network_groups(self, cdo_client: CDOClient) -> None:
        net_grps = cdo_client.get_objects(object_type="NETWORK_GROUP")
        assert net_grps

    def test_get_shared_network_objects(self, cdo_client: CDOClient) -> None:
        shared_net_objs = cdo_client.get_objects(object_type="*NETWORK*", issue_type="SHARED")
        assert shared_net_objs

    def test_get_all_protocol_objects(self, cdo_client: CDOClient) -> None:
        all_protocol_objs = cdo_client.get_objects(object_type="*PROTOCOL*")
        assert all_protocol_objs

    def test_get_protocol_group_objects(self, cdo_client: CDOClient) -> None:
        protocol_grp_objs = cdo_client.get_objects(object_type="PROTOCOL_GROUP")
        assert protocol_grp_objs

    def test_get_service_protocol_objects(self, cdo_client: CDOClient) -> None:
        svc_protocol_objs = cdo_client.get_objects(object_type="SERVICE_PROTOCOL_OBJECT")
        assert svc_protocol_objs
