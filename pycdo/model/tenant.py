from dataclasses import dataclass
from datetime import date, datetime
import calendar
from enum import Enum
from pydantic import BaseModel, Field
from typing import List


class ConflictDetectInterval(Enum):
    """Default interval at which CDO queries devices for changes. This value can be overridden per device."""

    twentyfour = "24 hours"
    onehour = "1 hour"
    sixhours = "6 hours"
    tenminutes = "10 minutes"


class BackupScheduleType(Enum):
    """Back up schedeule types"""

    recurring_schedule = "RecurringSchedule"


class ScheduleFrequency(Enum):
    weekly = "weekly"
    daily = "daily"
    monthly = "monthly"


class UserRole(Enum):
    admin = "admin"
    superadmin = "superadmin"
    edit = "editonly"
    deploy = "deployonly"
    read = "readonly"
    vpn = "vpnsessionmanager"
    api = "apionly"


class TenantUserRole(Enum):
    super_admin = "ROLE_SUPER_ADMIN"


class WorkFlowEvents(Enum):
    failed = "Failed"
    started = "Started"
    succeeded = "Succeeded"


class DeviceEvents(Enum):
    offline = "offline"
    online = "online"
    conflict = "conflict"
    ha_state = "hastatechanged"
    s2s = "sitetositedisconnected"


class TenantPayType(Enum):
    internal = "INTERNAL"


@dataclass
class BackupSchedule:
    """Backup Schedule settings"""

    frequency: ScheduleFrequency
    utc_time: datetime
    days: list[calendar.day_abbr]


@dataclass
class AlertSubscribers:
    email = str
    date_added = datetime


@dataclass
class AlertServiceIntegrations:
    """Alert service integrations (Webex, Slack, Custom...)"""

    name: str
    service_type: str
    webhook_url: str


@dataclass
class Notifications:
    """CDO Tenant notification settings"""

    device_events: list[DeviceEvents]
    deployment_events: list[WorkFlowEvents]
    backups: list[WorkFlowEvents]
    upgrades: list[WorkFlowEvents]
    subscribers: list[AlertSubscribers]
    integrations: list[AlertServiceIntegrations]


@dataclass
class CDOLogging:
    monthlyLimit: int
    amount_used: float
    days_left: int


@dataclass
class TenantPermissions:
    """/aegis/rest/v1/user/permissions"""


@dataclass
class TenantActivity:
    """/aegis/rest/v1/user/permissions"""


@dataclass
class FTDEULA:
    """FTD EULA"""

    status: bool
    username: str
    timestamp: datetime


@dataclass
class FTDBackupSchedule:
    """FTD Backup Schedule"""

    type_: BackupScheduleType
    repeat_type: ScheduleFrequency
    dayOfWeek: calendar.day_abbr
    daysOfWeek: list[calendar.day_abbr]
    days_of_month: int  # ?
    time: datetime  # 22:00


@dataclass
class TenantDeviceStatus:
    """https://www.defenseorchestrator.com/activity/device-status"""

    ftd_eula: FTDEULA


@dataclass
class TenentSettings:
    """Tenant Settings"""

    ftd_eula: FTDEULA
    auto_accept_oob_changes: bool
    auto_detect_rule_sets: bool
    schedule_deployments: bool
    ftd_backup_schedule: FTDBackupSchedule
    oob_check_interval: str  # enum


@dataclass
class TenantDeviceTypes:
    """https://www.defenseorchestrator.com/aegis/rest/v1/plugindevice/types"""

    # GENERIC_SSH
    # IOS


@dataclass
class TenantFeatures:
    # Features https://www.defenseorchestrator.com/aegis/rest/v1/features
    ignore_certificate: bool
    ftd_change_management: bool
    asa_sgt_from_cts_env_table: bool
    ftd_onboard_discovery: bool
    in_dev: bool
    dng_poc: bool
    rabbit_mq_support_request: bool
    ftd_netops_drilldown: bool
    ftd: bool
    cloud_device_gateway: bool
    asa_certificate_management: bool
    csmra_2: bool
    asac_new_policy_object_model: bool
    etherchannel_migration: bool
    template_params: bool
    aegis_to_aegis_over_aws: bool
    ftd_etherchannel: bool
    slim_shady_netconf_poc: bool
    asa_read_only_ra_vpn: bool
    user_group_auth: bool
    read_changelog_at_elasticsearch: bool
    shareable_template: bool
    ftd_onboard_token: bool
    asa_file_explorer: bool
    ftd_new_smartlicense_and_token_onboarding: bool
    ftd_ha: bool
    feature_for_tests: bool
    asa_security_group_tags: bool
    ftd_cleanup: bool
    wsa: bool
    asa_ra_vpn_crud: bool
    asa_configuration_object_migration: bool
    custom_ips: bool
    ftd_duo_ldap: bool
    swc_security_analytics: bool
    asa_time_range: bool
    fmc_microservice: bool
    ftd_enterprise_onboarding: bool
    test_feature_2: bool
    test_feature_1: bool
    notifications: bool
    asac: bool
    ftd_ha_upgrades: bool
    event_viewer_page: bool
    global_search_service: bool
    s2s_vpn_migration: bool
    ftd_config_import: bool
    changelog_cleanup: bool
    shared_policy: bool
    test_disable_duplicate_device_detection: bool
    csmra_2_ztna_sessions: bool
    talos_lookup: bool
    ftd_config_export: bool
    meraki_native_objects: bool
    disable_asa_user_agent_header: bool
    ftd_66: bool
    enterprise_ftd_movement: bool
    dedicated_remote_access_events_cluster: bool
    asac_2: bool
    boolata_poc: bool
    firepower_dev_versions: bool
    umbrella_onboarding: bool

    """

            "tenantSettings": {
                "ftdEula": {
                    "status": true,
                    "username": "aahackne@cisco.com",
                    "timestamp": "2021-02-18T17:42:22.732Z"
                }
            },
            "autoAcceptOobChanges": true,
            "autoDetectRuleSets": true,
            "scheduleDeployments": false,
            "ftdBackupSchedule": {
                "@type": "RecurringSchedule",
                "repeatType": "WEEKLY",
                "dayOfWeek": null,
                "daysOfWeek": [
                    "SUNDAY"
                ],
                "daysOfMonth": null,
                "time": "22:00"
            },
            "oobCheckInterval": "OOB_24_HOURS",
            "settings": {
                "aahackne@cisco.com": {
                    "numberOfLicenses": -1,
                    "allowedChangeLogSizeGigs": "1",
                    "eventsAllowedGbPerMonth": "450",
                    "userTenantRoles": [
                        "ROLE_SUPER_ADMIN"
                    ],
                    "tenantUid": "44dcd3bf-e608-40db-a588-e9150da988de",
                    "numberOfLicensesPerDeviceType": null,
                    "isTenantCustomSaml": false,
                    "originalTenantUid": null,
                    "username": "aahackne@cisco.com",
                    "tenantPayType": "INTERNAL",
                    "EVENTS_VIEWS": [
                        {
                            "id": "klcst72o",
                            "label": "View 1",
                            "data": {
                                "filters": [
                                    {
                                        "isActive": true,
                                        "id": "EV_INCLUDE_NET_FLOW_FILTER_CHECKBOX_ITEM",
                                        "label": "events.filters.includeNetFlow",
                                        "value": [
                                            "includeNetflowEvent"
                                        ],
                                        "sectionId": "includeNetFlow",
                                        "sectionLabel": "common.filters.events.netFlow.sectionTitle",
                                        "isRequired": true
                                    },
                                    {
                                        "id": "EV_TIME_RANGE_FILTER",
                                        "label": "common.filters.timeRanges.after",
                                        "value": [
                                            1630007256000,
                                            0
                                        ],
                                        "sectionId": "eventTimeRange",
                                        "sectionLabel": "events.filters.timeRange",
                                        "isRequired": true,
                                        "isActive": true
                                    }
                                ],
                                "columns": [
                                    {
                                        "isAlwaysVisible": true,
                                        "isVisibleByDefault": true,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "timestamp",
                                        "name": "Date/Time",
                                        "title": "Date/Time"
                                    },
                                    {
                                        "isAlwaysVisible": false,
                                        "isVisibleByDefault": true,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "DeviceType",
                                        "name": "Device Type",
                                        "title": "Device Type"
                                    },
                                    {
                                        "isAlwaysVisible": false,
                                        "isVisibleByDefault": true,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "EventType",
                                        "name": "Event Type",
                                        "title": "Event Type"
                                    },
                                    {
                                        "isAlwaysVisible": false,
                                        "isVisibleByDefault": true,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "SensorID",
                                        "name": "Sensor ID",
                                        "title": "Sensor ID"
                                    },
                                    {
                                        "isAlwaysVisible": false,
                                        "isVisibleByDefault": true,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "InitiatorIP",
                                        "name": "Initiator IP",
                                        "title": "Initiator IP"
                                    },
                                    {
                                        "isAlwaysVisible": false,
                                        "isVisibleByDefault": true,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "ResponderIP",
                                        "name": "Responder IP",
                                        "title": "Responder IP"
                                    },
                                    {
                                        "isAlwaysVisible": false,
                                        "isVisibleByDefault": true,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "ResponderPort",
                                        "name": "Port",
                                        "title": "Port"
                                    },
                                    {
                                        "isAlwaysVisible": false,
                                        "isVisibleByDefault": true,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "Protocol",
                                        "name": "Protocol",
                                        "title": "Protocol"
                                    },
                                    {
                                        "isAlwaysVisible": false,
                                        "isVisibleByDefault": true,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "Action",
                                        "name": "Action",
                                        "title": "Action"
                                    },
                                    {
                                        "isAlwaysVisible": false,
                                        "isVisibleByDefault": true,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "Policy",
                                        "name": "Policy",
                                        "title": "Policy"
                                    },
                                    {
                                        "isAlwaysVisible": false,
                                        "isVisibleByDefault": false,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "Application",
                                        "name": "Application",
                                        "title": "Application"
                                    },
                                    {
                                        "isAlwaysVisible": false,
                                        "isVisibleByDefault": false,
                                        "isVisible": true,
                                        "isVisibleInColumnMenu": true,
                                        "prop": "WebApplication",
                                        "name": "Web Application",
                                        "title": "Web Application"
                                    }
                                ]
                            },
                            "isEditing": false
                        }
                    ],
                    "EVENTS_DISABLE_AUTO_SHOW_HELP": true,
                    "sseTenantUid": "44dcd3bf-e608-40db-a588-e9150da988de"
                }
            },
            "notificationsSettings": {
                "eventSubscriptionState": {
                    "DEPLOY": [],
                    "BACKUP": [],
                    "UPGRADE": []
                },
                "discoverySubscriptionState": {
                    "ENTERED_HA_FAILOVER_MODE": false,
                    "RETURNED_HA_PRIMARY_MODE": false,
                    "CONNECTIVITY_LOST": false,
                    "CONNECTIVITY_FOUND": false,
                    "CONFLICT_DETECTED": false
                },
                "actionRequiredSubscriptionState": {
                    "CHANGE_MANAGER_PENDING": false
                },
                "subscribers": [],
                "lastReadNotificationTimestamp": 0
            }
        }
    ]4
    """


@dataclass
class CDOUser:
    username: str


@dataclass
class UserSettings:
    """Per user tenant settings"""

    numberOfLicenses: int
    allowedChangeLogSizeGigs: int
    eventsAllowedGbPerMonth: int
    userTenantRoles: list[TenantUserRole]
    tenantUid: str
    numberOfLicensesPerDeviceType: int
    isTenantCustomSaml: bool
    originalTenantUid: str
    tenantPayType: TenantPayType


def __init__(self) -> None:
    pass
