from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from pycdo.model.cdo import CDOContext
import logging

log = logging.getLogger(__name__)


class TenantUserRole(Enum):
    super_admin = "ROLE_SUPER_ADMIN"
    admin = "ROLE_ADMIN"
    read_only = "ROLE_READ_ONLY"
    edit_only = "ROLE_EDIT_ONLY"
    deploy_only = "ROLE_DEPLOY_ONLY"
    vpn_manager = "ROLE_VPN_SESSIONS_MANAGER"


class Services(Enum):
    msp_portal = "MSP_PORTAL"
    cdo = "CDO"
    cdo_migration = "CDO_MIGRATION"


class Tenants(BaseModel):
    uid: str
    name: str
    organization_name: Optional[str] = Field(alias="organizationName")
    services: List[Services]


class TenantUser(BaseModel):
    """User data model as defined in a CDO tenant"""

    uid: str
    name: str
    username: Optional[str]
    roles: List[TenantUserRole]
    api_token_id: Optional[str] = Field(alias="apiTokenId")
    is_api_only_user: bool = Field(alias="isApiOnlyUser")
    lastSuccessfulLogin: Optional[datetime] = Field(alias="lastSuccessfulLogin")

    class Config:
        use_enum_values = True


class TenantContext(CDOContext):
    """CDO tenant data model /aegis/rest/v1/services/common/tenantcontext"""

    eula_status: bool = Field(alias="eulaStatus")
    eula_username: Optional[str] = Field(alias="eulaUsername")
    eula_timestamp: Optional[datetime] = Field(alias="eulaTimestamp")
    last_full_indexing_date: Optional[datetime] = Field(alias="lastFullIndexingDate")
    tenant_settings: Optional[dict] = Field(alias="tenantSettings")
    auto_accept_oob_changes: bool = Field(alias="autoAcceptOobChanges")
    auto_detect_ruleSets: bool = Field(alias="autoDetectRuleSets")
    schedule_deployments: bool = Field(alias="scheduleDeployments")
    ftd_backup_schedule: Optional[dict] = Field(alias="ftdBackupSchedule")
    oob_check_interval: str = Field(alias="oobCheckInterval")
    settings: dict  # TODO: enum
    notificationsSettings: dict  # TODO: enum


class ContextObject(CDOContext):
    password: Optional[str]
    roles: List[str]  # TODO
    is_locked: bool = Field(alias="isLocked")
    attemptCounter = int
    last_login_attempt: Optional[datetime] = Field(alias="lastLoginAttempt")
    is_api_only_user: Optional[bool] = Field(alias="isApiOnlyUser")


class UserContext(CDOContext):
    """User contexts returned when creating a new user"""

    source: dict  # TODO uid: str, namespace: 'namespace', type: 'users'
    target: dict  # TODO uid: str, namespace: 'namespace', type: 'tenants'
    source_object: Optional[dict] = Field(alias="sourceObject")  # TODO
    target_object: Optional[dict] = Field(alias="targetObject")  # TODO
