import enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CDOContext(BaseModel):
    """Common CDO Context arrtibutes"""

    tags: Optional[dict]
    tag_keys: Optional[list] = Field(alias="tagKeys")
    tag_values: Optional[list] = Field(alias="tagValues")
    uid: str
    name: Optional[str]
    namespace: str
    type: str  # TODO: enum
    version: int
    created_date: Optional[datetime] = Field(alias="createdDate")
    last_updated_date: Optional[datetime] = Field(alias="lastUpdatedDate")
    action_context: Optional[dict] = Field(alias="actionContext")  # TODO
    state: Optional[str]
    trigger_state: Optional[str] = Field(alias="triggerState")
    queue_trigger_state: Optional[str] = Field(alias="queueTriggerState")
    state_machine_context: Optional[str] = Field(alias="stateMachineContext")
    state_date: Optional[datetime] = Field(alias="stateDate")
    status: Optional[str]  # TODO: enum
    state_machine_details: Optional[dict] = Field(alias="stateMachineDetails")
    scheduled_state_machine_enabled_map: Optional[dict] = Field(alias="scheduledStateMachineEnabledMap")
    pending_states_queue: Optional[list] = Field(alias="pendingStatesQueue")
    created_tenant_uid: Optional[str] = Field(alias="createdTenantUid")
    last_successful_login: Optional[datetime] = Field(alias="lastSuccessfulLogin")
    credentials: Optional[dict]
    model: Optional[bool]
