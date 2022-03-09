from dataclasses import dataclass
from datetime import datetime


@dataclass
class EventFilters:
    isActive: bool
    id: str
    lable: str
    value: list[str]  # TODO: enum values includeNetflowEvent
    sectionId: str  # TODO enum
    sectionLabel: str  # TODO enum
    isRequired: bool
    isActive: bool
    isEditing: bool


@dataclass
class EventColumns:
    isAlwaysVisible: bool
    isVisibleByDefault: bool
    isVisible: bool
    isVisibleInColumnMenu: bool
    prop: str
    name: str
    title: str


@dataclass
class EventSubscriptionState:
    DEPLOY: list
    BACKUP: list
    UPGRADE: list


@dataclass
class DiscoverySubscriptionState:
    ENTERED_HA_FAILOVER_MODE: bool
    RETURNED_HA_PRIMARY_MODE: bool
    CONNECTIVITY_LOST: bool
    CONNECTIVITY_FOUND: bool
    CONFLICT_DETECTED: bool


@dataclass
class ActionRequiredSubscriptionState:
    CHANGE_MANAGER_PENDING: bool


@dataclass
class Notifications:
    eventSubscriptionState: EventSubscriptionState
    discoverySubscriptionState: DiscoverySubscriptionState
    actionRequiredSubscriptionState: dict
    subscribers: list
    lastReadNotificationTimestamp: datetime


@dataclass
class EventsViews:
    """Event viewer settings"""

    id: str
    lable: str
    data: dict  # TODO: Model event views....


def __init__(self) -> None:
    pass
