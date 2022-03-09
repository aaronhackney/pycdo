from pycdo.base import CDOBaseClient
from pycdo.model.change_logs import ChangeLog
from typing import List
import logging

logger = logging.getLogger(__name__)


class CDOChangeLogs(CDOBaseClient):
    """Class for getting changelogs from a CDO tenant"""

    def build_query(self, **kwargs):
        """Returns a query string used to filter/search changelogs for specific things

        Args:
            **kwargs: optional keyward arguments
                user (str, optional): filter on the given username
                change_log_state (str, optional): filter on the changelog state [COMPLETED, ACTIVE]
                change_log_event_action (str, optional): The types of events to retrieve [DELETE, UPDATE]
                start_time (int, optional): Beginning EPOCH time [ int(timedate.timestamp()) ] to search for
                end_time (int, optional): Ending EPOCH time [ int(timedate.timestamp()) ] to search for

        Returns:
            str: returns a query string or None
        """
        query = []
        # events.user.keyword:"aahackne@cisco.com"
        query.append(f"events.user.keyword:\"{kwargs.get('user')}\"") if "user" in kwargs else None
        query.append(kwargs.get("change_log_state")) if "change_log_state" in kwargs else None
        query.append(kwargs.get("change_log_event_action")) if "change_log_event_action" in kwargs else None
        time_range = self._get_time_range(**kwargs)  # Get time range query options if presented
        query.append(time_range) if time_range else None

        if len(query) > 1:  # Return a compund query string
            return " AND ".join(["(" + line + ")" for line in query])
        elif len(query) == 1:  # return a simple, single query
            return query[0]

    def _get_time_range(self, **kwargs):
        if "start_time" in kwargs or "end_time" in kwargs:
            start_time = int(kwargs.get("start_time") * 1000) if "start_time" in kwargs else "*"
            end_time = int(kwargs.get("end_time") * 1000) if "end_time" in kwargs else "*"
            return f"lastEventTimestamp:[{start_time} TO {end_time}]"

    def get_changelogs(self, **kwargs):
        """Get change logs from CDO

        Args:
            limit (int, optional): number of records to return at one time. Defaults to 100 (API MAX = 200)
            offset (int, optional): useful for paging records over multiple api calls. Defaults to 0.
            sort (str, optional): Order in which to sort the returned records. Defaults to "lastEventTimestamp:desc".
            user (str, optional): filter on the given username
            change_log_state (str, optional): filter on the changelog state [COMPLETED, ACTIVE]
            change_log_event_action (str, optional): The types of events to retrieve [DELETE, UPDATE]
            start_time (datetime, optional): Beginning EPOCH time to search for
            end_time (datetime, optional): Ending EPOCH time to search for
            resolve (str, optional): define which fields to return. Defaults to uid,name,lastEventTimestamp,
                                     changeLogState,objectReference,lastEventDescription,lastEventUser,events

        Returns:
            list: return a list containing log objects
        """
        offset = kwargs.get("offset") if "offset" in kwargs else 0
        sort = kwargs.get("sort") if "sort" in kwargs else "lastEventTimestamp:desc"
        limit = kwargs.get("limit") if "limit" in kwargs else 100
        resolve = (
            kwargs.get("resolve")
            if "resolve" in kwargs
            else (
                "[changelogs/query.{uid,name,lastEventTimestamp,changeLogState,objectReference,"
                "lastEventDescription,lastEventUser,events}]"
            )
        )
        params = {
            "q": self.build_query(**kwargs),
            "limit": limit,
            "offset": offset,
            "resolve": resolve,
            "sort": sort,
        }
        logs = self.get_operation(f"{self.PREFIX_LIST['CHANGELOG_QUERY']}", params=params)  # prime the loop
        change_logs = []
        while True:
            change_logs = change_logs + logs
            if len(logs) == limit:  # We got the limit of records there may be more!
                params["offset"] = params["offset"] + limit  # get the next batch of records
                logs = self.get_operation(f"{self.PREFIX_LIST['CHANGELOG_QUERY']}", params=params)
            else:
                break
        return [ChangeLog(**log) for log in change_logs]  # return ChangeLog objects

    def get_cli_logs(self, logs: List[ChangeLog]) -> List[ChangeLog]:
        """Given a list of ChangeLog objects, return only the ChangeLog objects with "CLI Execution" events

        Args:
            logs (List[ChangeLog]): List of ChangeLog objects

        Returns:
            List[ChangeLog]: List of ChangeLog objects
        """
        return_logs = []
        for log in logs:
            for event in log.events:
                if event.details.description == "CLI Execution":
                    return_logs.append(log)
        return return_logs
