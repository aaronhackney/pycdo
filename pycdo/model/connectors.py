from typing import Optional
from pycdo.model.cdo import CDOContext
from pydantic import Field, BaseModel
from datetime import datetime


class LarPublicKey(BaseModel):
    encoded_key: Optional[str] = Field(alias="encodedKey")
    version: Optional[int]
    key_id: Optional[str] = Field(alias="keyId")


class Connector(CDOContext):
    rabbit_mq_details: Optional[dict] = Field(alias="rabbitMQDetails")
    tenant_uid: Optional[str] = Field(alias="tenantUid")
    last_heartbeat_time: Optional[datetime] = Field(alias="last_heartbeat_time")
    service_connectivity_state: Optional[str] = Field(alias="service_connectivity_state")
    ip_address: Optional[str] = Field(alias="ipAddress")
    container_ip_address: Optional[str] = Field(alias="containerIpAddress")
    lar_public_key: Optional[LarPublicKey] = Field(alias="larPublicKey")
    lar_status: Optional[str] = Field(alias="larStatus")
    on_prem_lar_configured: Optional[bool] = Field(alias="onPremLarConfigured")
    lar_version: Optional[str] = Field(alias="larVersion")
    lar_image: Optional[str] = Field(alias="larImage")
    sha256: Optional[str]
    lar_metadata: Optional[dict] = Field(alias="larMetadata")
    lar_migrations: Optional[dict] = Field(alias="larMigrations")
    default_lar: Optional[bool] = Field(alias="defaultLar")
    cdg: Optional[bool]
    sns_sqs_details: Optional[dict] = Field(alias="snsSqsDetails")
    latest_aegis_signature_key: Optional[dict] = Field(alias="latestAegisSignatureKey")
    latest_aegis_encryption_key: Optional[dict] = Field(alias="latestAegisEncryptionKey")
