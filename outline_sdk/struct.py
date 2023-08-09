from typing import Optional

from dataclasses import dataclass


@dataclass
class AccessKey:
    id: str
    name: str
    password: str
    port: int
    method: str
    access_url: str

    metrics: Optional[int] = None


@dataclass
class ServerInfo:
    name: str
    server_id: str
    metrics_enabled: bool
    created_at: str
    version: str

    port: int
    host: str
