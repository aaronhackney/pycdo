from pycdo import CDOClient
from datetime import datetime


class TestCDOChangeLogs:
    """Test depend on logs exising in the tenant for the give parameters/users/time windows provided"""

    USER = "aahackne@cisco.com"

    def test_get_all_change_logs(self, cdo_client: CDOClient) -> None:
        change_logs = cdo_client.get_changelogs()
        assert change_logs

    def test_get_change_logs_date_from_range(self, cdo_client: CDOClient) -> None:
        start_time = datetime(2021, 1, 1, 00, 00, 00)  # Search for everything since 1/1/2021
        change_logs = cdo_client.get_changelogs(start_time=int(start_time.timestamp()))
        assert change_logs

    def test_get_change_logs_date_to_range(self, cdo_client: CDOClient) -> None:
        end_time = datetime(2022, 1, 1, 00, 00, 00)  # Search for everything until 1/1/2022
        change_logs = cdo_client.get_changelogs(end_time=int(end_time.timestamp()))
        assert change_logs

    def test_get_change_logs_date_range(self, cdo_client: CDOClient) -> None:
        start_time = datetime(2021, 3, 1, 00, 00, 00)  # Search for everything since 3/1/2021
        end_time = datetime(2021, 4, 1, 00, 00, 00)  # Search for everything until 4/1/2021
        change_logs = cdo_client.get_changelogs(
            start_time=int(start_time.timestamp()), end_time=int(end_time.timestamp())
        )
        assert change_logs

    def test_get_change_logs_by_user(self, cdo_client: CDOClient) -> None:
        change_logs = cdo_client.get_changelogs(user=self.USER)
        assert change_logs

    def test_get_by_user_and_time_range(self, cdo_client: CDOClient) -> None:
        start_time = datetime(2021, 3, 1, 00, 00, 00)  # Search for everything since 3/1/2021
        end_time = datetime(2021, 4, 1, 00, 00, 00)  # Search for everything until 4/1/2021
        change_logs = cdo_client.get_changelogs(
            start_time=int(start_time.timestamp()),
            end_time=int(end_time.timestamp()),
            user=self.USER,
        )
        assert change_logs

    def test_get_cli_logs(self, cdo_client: CDOClient) -> None:
        change_logs = cdo_client.get_changelogs()
        cli_logs = cdo_client.get_cli_logs(change_logs)
        assert cli_logs
