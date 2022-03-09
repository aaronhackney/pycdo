from typing import Optional, List
from pycdo.model.cdo import CDOContext
from pydantic import Field, BaseModel
from datetime import datetime
from enum import Enum


class OnboardingMethod(Enum):
    serial = "Serial Number"
    token = "token"


# TODO Does this need to be ASA specific or generic device?
class ASAInterface(BaseModel):
    name: Optional[str]
    ipaddress: Optional[str]
    subnet_mask: Optional[str] = Field(alias="subnetMask")
    object_name: Optional[str] = Field(alias="objectName")
    is_active: Optional[bool] = Field(alias="isActive")


class Device(CDOContext):
    # TODO: verify these data types
    # TODO: enum where it makes sense
    associated_device_uid: Optional[str] = Field(alias="associatedDeviceUid")
    sse_enabled: Optional[bool] = Field(alias="sseEnabled")
    device_role: Optional[str] = Field(alias="deviceRole")
    sse_device_registration_token: Optional[dict] = Field(alias="sseDeviceRegistrationToken")
    sse_device_serial_number_registration: Optional[dict] = Field(alias="sseDeviceSerialNumberRegistration")
    sse_device_data: Optional[dict] = Field(alias="sseDeviceData")
    disks: Optional[list]
    failover_disks: Optional[list] = Field(alias="failoverDisks")
    custom_links: Optional[list] = Field(alias="customLinks")
    should_init_creds: Optional[bool] = Field(alias="shouldInitCreds")
    ipv4: Optional[str]
    interfaces: Optional[str]
    device_activity: Optional[dict] = Field(alias="deviceActivity")
    serial: Optional[str]
    chassis_serial: Optional[str] = Field(alias="chassisSerial")
    software_version: Optional[str] = Field(alias="softwareVersion")
    sse_device_serial_number_registration: Optional[dict] = Field(alias="sseDeviceSerialNumberRegistration")
    connectivity_state: Optional[int] = Field(alias="connectivityState")
    connectivity_error: Optional[str] = Field(alias="connectivityError")
    ignore_certificate: Optional[bool] = Field(alias="ignoreCertificate")
    config: Optional[str]
    most_recent_device_config: Optional[dict] = Field(alias="mostRecentDeviceConfig")
    device_config_on_disk: Optional[dict] = Field(alias="deviceConfigOnDisk")
    device_config: Optional[str] = Field(alias="deviceConfig")
    certificate: Optional[str] = Field(alias="certificate")
    most_recent_certificate: Optional[str] = Field(alias="mostRecentCertificate")
    config_hash: Optional[str] = Field(alias="configHash")
    config_state: Optional[str] = Field(alias="configState")
    config_processing_state: Optional[str] = Field(alias="configProcessingState")
    enable_oob_detection: Optional[bool] = Field(alias="enableOobDetection")
    oob_detection_state: Optional[str] = Field(alias="oobDetectionState")
    last_oob_detection_startedAt: Optional[datetime] = Field(alias="lastOobDetectionStartedAt")
    last_oob_detection_suspended_at: Optional[datetime] = Field(alias="lastOobDetectionSuspendedAt")
    auto_accept_oob_enabled: Optional[bool] = Field(alias="autoAcceptOobEnabled")
    model_number: Optional[str] = Field(alias="modelNumber")
    model: Optional[str]
    device_type: Optional[str] = Field(alias="deviceType")
    device_sub_type: Optional[str] = Field(alias="deviceSubType")
    has_firepower: Optional[bool] = Field(alias="hasFirepower")
    last_error_map: Optional[dict] = Field(alias="lastErrorMap")
    logs: Optional[dict]
    notes: Optional[dict]
    metadata: Optional[dict]
    customData: Optional[dict]
    configuration_reference: Optional[dict] = Field(alias="configurationReference")
    oob_check_interval: Optional[str] = Field(alias="oobCheckInterval")
    lar_uid: Optional[str] = Field(alias="larUid")
    lar_type: Optional[str] = Field(alias="larType")
    last_deploy_timestamp: Optional[datetime] = Field(alias="lastDeployTimestamp")
    port: Optional[str]
    host: Optional[str]
    logging_enabled: Optional[bool] = Field(alias="loggingEnabled")
    live_asa_device: Optional[bool] = Field(alias="liveAsaDevice")


# TODO: verify these data types
class ASADevice(Device):
    asa_interfaces: Optional[List[ASAInterface]] = Field(alias="asaInterfaces")
    time_ranges: Optional[list] = Field(alias="timeRanges")
    vpn_uid: Optional[str] = Field(alias="vpnUid")
    selected_interface_object: Optional[dict] = Field(alias="selectedInterfaceObject")
    selected_interface_ip: Optional[str] = Field(alias="selectedInterfaceIP")
    security_context_mode: Optional[str] = Field(alias="securityContextMode")
    metadata: Optional[dict]
    crypto_checksum: Optional[str] = Field(alias="cryptoChecksum")
    device_config_crypto_checksum: Optional[str] = Field(alias="deviceConfigCryptoChecksum")
    named_references: Optional[list] = Field(alias="namedReferences")
    object_version: Optional[int] = Field(alias="objectVersion")
    asac_config_generations_hash: Optional[str] = Field(alias="asacConfigGenerationsHash")


class FTDDevice(Device):
    # TODO: verify these data types
    # TODO: enum and subclass where it makes sense
    license_requirements: Optional[List[dict]] = Field(alias="licenseRequirements")
    info: Optional[dict]
    platform_info: Optional[dict] = Field(alias="platformInfo")
    template_uid: Optional[str] = Field(alias="templateUid")
    template_type: Optional[str] = Field(alias="templateType")
    policy_version: Optional[str] = Field(alias="policyVersion")
    objects_map: Optional[dict] = Field(alias="objectsMap")
    currDeployment_uid: Optional[str] = Field(alias="currDeploymentUid")
    ftd_recurring_ips_rule_update_imports: Optional[dict] = Field(alias="ftdRecurringIpsRuleUpdateImports")
    metadata: Optional[dict]
    supported_features: Optional[dict] = Field(alias="supportedFeatures")
    last_saved_policy_json: Optional[dict] = Field(alias="lastSavedPolicyJson")
    temp_registration_field: Optional[str] = Field(alias="tempRegistrationField")
    ftd_ha_metadata: Optional[dict] = Field(alias="ftdHaMetadata")
    primary_device_details: Optional[dict] = Field(alias="primaryDeviceDetails")
    secondary_device_details: Optional[dict] = Field(alias="secondaryDeviceDetails")
    primary_ftd_ha_status: Optional[dict] = Field(alias="primaryFtdHaStatus")
    secondary_ftd_ha_status: Optional[dict] = Field(alias="secondaryFtdHaStatus")
    ftd_ha_error: Optional[dict] = Field(alias="ftdHaError")
    ftd_smart_license_status: Optional[dict] = Field(alias="ftdSmartLicenseStatus")
    ha_combined_device: Optional[bool] = Field(alias="haCombinedDevice")
