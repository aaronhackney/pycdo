from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: Optional[str]
    expires_in: Optional[datetime]
    scope: Optional[str]
    tenant_uuid: Optional[str] = Field(alias="TenantUid")
    tenant_name: Optional[str] = Field(alias="TenantName")
