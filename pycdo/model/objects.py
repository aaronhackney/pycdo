from pycdo.model.cdo import CDOContext
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class ObjectType(Enum):
    "Object Types"
    NETWORK_OBJECT = "NetworkObject"
    GROUP_NETWORK_OBJECT = "Group:NetworkObject"
    SERVICE_OBJECT = "ServiceObject"
    GROUP_SERVICE_OBJECT = "Group:ServiceObject"
    TAG_OBJECT = "TagObject"
    GROUP_TAG_OBJECT = "Group:TagObject"
    URL_OBJECT = "URLObject"
    GROUP_URL_OBJECT = "Group:URLObject"
    IP_LIST_OBJECT = "IPListObject"
    APPLICATION_FILTER = "ApplicationFilter"
    FILE_LIST = "FileList"
    SECURITY_ZONES = "SecurityZones"


class NetworkObject(CDOContext):
    """Network Objects"""

    # TODO: Alias
    deleted: Optional[bool]
    objectType: Optional[str]  # need to enum
    cdoInternal: Optional[bool]
    isReadOnly: Optional[bool]
    metadata: Optional[dict]
    searchableDetails: Optional[dict]
    parameterizedFields: Optional[dict]
    deviceUid: Optional[str]
    configurationUid: Optional[str]
    sourceConfigurationUid: Optional[str]
    deviceType: Optional[str]  # ASA enum
    contents: Optional[list]
    overrideContents: Optional[list]
    elements: Optional[list]
    description: Optional[str]
    enabled: Optional[bool]
    digest: Optional[str]
    elementDigest: Optional[str]
    issues: Optional[list]
    issueType: Optional[str]
    ignoredIssues: Optional[list]
    syncStatus: Optional[str]  # SYNCED, enum
    operationType: Optional[str]  # enum
    allContentUUIDs: Optional[list]
    allObjectReferenceContentUUIDs: Optional[list]
    readOnly: Optional[bool]
    references: Optional[list]
    deviceUids: Optional[list]
    issueDigest: Optional[str]
    issueType: Optional[str]
    overrides: Optional[list]
