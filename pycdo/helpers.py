import os

# TODO: Make the version a variable
PREFIX_LIST = {
    "CHANGELOG_QUERY": "/aegis/rest/changelogs/query",
    "DEBUGGING": "/aegis/rest/v1/services/state-machines/debugging",
    "DEVICE": "/aegis/rest/v1/device",  # Maps instance device (eg ASA, FTD) to Target Device
    "TARGET_DEVICES": "/aegis/rest/v1/services/targets/devices",  # Target Device represents the actual object in CDO
    "ACCESS_GROUPS": "/aegis/rest/v1/services/targets/accessgroups",
    "ASA_DEVICES_CONFIGS": "/aegis/rest/v1/services/asa/devices-configs",
    "ASA_CONFIGS": "/aegis/rest/v1/services/asa/configs",
    "INSTANCES": "/aegis/rest/v1/services/state-machines/instances",
    "JOBS": "/aegis/rest/v1/services/state-machines/jobs",
    "MSSP_DEVICES": "/api/theia/v1/devices",
    "MSSP_ENV": "edge.us.cdo.cisco.com",
    "MSSP_TENANTS": "/api/theia/v1/tenants",
    "OBJECTS": "/aegis/rest/v1/services/targets/objects",
    "CONNECTORS": "/aegis/rest/v1/services/targets/proxies",
    "SERVICES": "/aegis/rest/v1/services",
    "TENANTS": "/anubis/rest/v1/user/tenants",
    "TENANT_AUTH": "/anubis/rest/v1/oauth",
    "TENANT_CONTEXT": "/aegis/rest/v1/services/common/tenantcontext",
    "TENANT_USERS": "/anubis/rest/v1/users",
    "WORKINGSET": "/aegis/rest/v1/services/common/workingset",
}

# move to enum in appropriate class
DEVICE_TYPES = {
    "ASA": "deviceType:ASA OR (deviceSubType:ASA)",
    "FTD": "FTD OR (deviceSubType:FTD)",
    "FIREPOWER": "FIREPOWER OR (deviceSubType:FIREPOWER)",
    "AWS": "AWS_VPC OR (deviceSubType:AWS_VPC)",
    "MERAKI": "MERAKI_SECURITY_APPLIANCE OR (deviceSubType:MERAKI_SECURITY_APPLIANCE)",
    "UMBRELLA": "UMBRELLA OR (deviceSubType:UMBRELLA)",
}

# move to enum in appropriate class
CONNECTIVITY_STATE = {
    8: "CHANGED_CERT_ACCEPTED",
    7: "PENDING_CHANGED_CERT_ACCEPTANCE",
    6: "COMPLETED_CREDENTIAL_STORAGE",
    -16: "ATTACHED_TO_TEMPLATE",
    -14: "INSUFFICIENT_LICENSES",
    -13: "INVALID_SERIAL_NUMBER",
    -12: "UNREGISTERED",
    -11: "UNSUPPORTED_VERSION",
    -10: "PENDING_CERT_RETRIEVAL_AFTER_RELOAD",
    -9: "WAITING_FOR_DEVICE_TO_COME_BACK_ONLINE",
    -8: "PENDING_WAIT_FOR_RELOAD_TO_BEGIN",
    -7: "DUPLICATE_DEVICE",
    -6: "GENERIC_ERROR",
    -5: "UNKNOWN",
    -4: "BAD_CREDENTIALS",
    -2: "UNREACHABLE",
    -1: "PENDING",
    0: "OFFLINE",
    1: "ONLINE",
    2: "ONBOARDING",
    3: "VALIDATING_CERT",
    4: "CERT_VALIDATED",
    9: "PENDING_ONBOARDING_SETUP",
    -15: "PARTIALLY_ONLINE",
    -17: "INCORRECT_PERMISSIONS",
    -18: "DELETED",
    999: "DEFAULT",
}
