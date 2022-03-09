from typing import Optional, List
from pycdo.model.cdo import CDOContext
from pydantic import Field, BaseModel
from datetime import datetime


class EventDetails(BaseModel):
    description: Optional[str]
    extended_details: Optional[str] = Field("", alias="extendedDetails")


class Event(BaseModel):
    user: Optional[str]
    details: Optional[EventDetails]
    change_log_event_action: Optional[str] = Field(alias="changeLogEventAction")
    event_date: datetime = Field(alias="eventDate")


class ChangeLog(CDOContext):
    # TODO: verify these data types
    # TODO: enum where it makes sense
    change_log_state: Optional[str] = Field(alias="changeLogState")
    object_reference: Optional[dict] = Field(alias="objectReference")
    extra_info: Optional[dict] = Field(alias="extraInfo")
    last_event_timestamp: Optional[datetime] = Field(alias="lastEventTimestamp")
    last_event_user: Optional[str] = Field(alias="lastEventUser")
    last_event_description: Optional[str] = Field(alias="lastEventDescription")
    in_es: Optional[bool] = Field(alias="inES")
    events: Optional[List[Event]]
    change_request_names: Optional[list] = Field(alias="changeRequestNames")
    change_requests_mapper_uid: Optional[str] = Field(alias="changeRequestsMapperUid")
