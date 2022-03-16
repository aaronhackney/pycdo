from typing import Optional, List
from pycdo.model.devices import Device, DeviceConfig, ASADevice
from pydantic import Field, BaseModel


class ASA(BaseModel):
    """Building block for Abstracted ASA Device"""

    name: str
    target_device: Optional[Device]
    device_config: Optional[DeviceConfig]
    asa: Optional[ASADevice]
