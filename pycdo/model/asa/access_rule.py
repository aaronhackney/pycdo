from typing import Optional, List
from pycdo.model.cdo import CDOContext
from pydantic import Field, BaseModel
from datetime import datetime
from enum import Enum


class AccessRuleContent(BaseModel):
    """Building block for AccessRule"""

    name: Optional[str]
    contentUid: Optional[str] = Field(alias="contentUid")
    contentType: Optional[str] = Field(alias="contentType")
    contentDigest: Optional[str] = Field(alias="contentDigest")


class LogSettings(BaseModel):
    """Building block for AccessRule"""

    level: Optional[str]
    interval: Optional[int]


class AccessRule(BaseModel):
    rule_action: Optional[AccessRuleContent] = Field(alias="ruleAction")
    protocol: Optional[AccessRuleContent]
    source_security_group: Optional[AccessRuleContent] = Field(alias="sourceSecurityGroup")
    source_address: Optional[AccessRuleContent] = Field(alias="sourceAddress")
    source_port: Optional[AccessRuleContent] = Field(alias="sourcePort")
    destination_security_group: Optional[AccessRuleContent] = Field(alias="destinationSecurityGroup")
    destination_address: Optional[AccessRuleContent] = Field(alias="destinationAddress")
    destination_port: Optional[AccessRuleContent] = Field(alias="destinationPort")
    icmp_argument: Optional[AccessRuleContent] = Field(alias="icmpArgument")
    enabled: Optional[bool]
    log_settings: Optional[LogSettings] = Field(alias="logSettings")
    timerange_argument: Optional[AccessRuleContent] = Field(alias="timerangeArgument")
    remark: Optional[str]
    issues: Optional[list]
    access_control_entries_count: Optional[int] = Field(alias="accessControlEntriesCount")
    line_num: Optional[int] = Field(alias="lineNum")
    content_uuids: Optional[List[str]] = Field(alias="contentUUIDs")
    referenced_contents: Optional[list] = Field(alias="referencedContents")


class AccessGroup(CDOContext):
    access_rules: Optional[List[AccessRule]] = Field(alias="accessRules")
    shared: Optional[bool]
    shared_detector_digest: Optional[str] = Field(alias="sharedDetectorDigest")
    editable: Optional[bool]
    properties: Optional[dict]
    num_access_rules: Optional[int] = Field(alias="numAccessRules")
    issue_types: Optional[list] = Field(alias="issueTypes")
    issue_counts: Optional[int] = Field(alias="issueCounts")
    access_control_entry_counts: Optional[dict] = Field(alias="accessControlEntryCounts")  # TODO: model
    digests: Optional[list]
    global_remark: Optional[str] = Field(alias="globalRemark")
    asa_interfaces: Optional[list] = Field(alias="asaInterfaces")
    directions: Optional[list]
    device_uid: Optional[str] = Field(alias="deviceUid")
    edited_object_uids: Optional[list] = Field(alias="deviceUids")
    device_uids: Optional[list] = Field(alias="deviceUids")
    issue_digest: Optional[str] = Field(alias="issueDigest")
    content_uuids: Optional[list] = Field(alias="contentUUIDs")
    referenced_contents: Optional[list] = Field(alias="referencedContents")
