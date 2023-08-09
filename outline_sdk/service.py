from typing import List, Dict, Optional

from .client import Client
from .struct import AccessKey, ServerInfo


def map_access_key(**raw_data) -> AccessKey:
    return AccessKey(
        id=raw_data['id'],
        name=raw_data['name'],
        password=raw_data['password'],
        port=raw_data['port'],
        method=raw_data['method'],
        access_url=raw_data['accessUrl'],

        metrics=raw_data.get('metrics'),
    )


class Service:
    def __init__(self, *, url: str, cert_sha256: str):
        self.api = Client(url=url, cert_sha256=cert_sha256)

    async def get_keys(self, include_metrics: bool = False) -> List[AccessKey]:
        response = await self.api.get_keys()

        metrics = {}
        if include_metrics:
            metrics = await self.metrics_transfer()

        result = []
        for key in response.json['accessKeys']:
            result.append(map_access_key(
                **key,
                **{'metrics': metrics.get(key['id'])}
            ))

        return result

    async def metrics_transfer(self) -> Dict[str, int]:
        metrics_raw = await self.api.metrics_transfer()
        return metrics_raw.json['bytesTransferredByUserId'] or {}

    async def create_key(self, name: Optional[str] = None) -> AccessKey:
        response = await self.api.create_key()
        new_key = map_access_key(**response.json)

        if name:
            await self.api.rename_key(new_key.id, name)
            new_key.name = name

        return new_key

    async def rename_key(self, key_id: str, name: str) -> bool:
        res = await self.api.rename_key(key_id, name)
        return res.code == 204

    async def delete_key(self, key_id: str) -> bool:
        res = await self.api.delete_key(key_id)
        return res.code == 204

    async def set_data_limit(self, key_id: str, limit_bytes: int) -> bool:
        res = await self.api.set_data_limit(key_id, limit_bytes)
        return res.code == 204

    async def delete_data_limit(self, key_id: str) -> bool:
        res = await self.api.delete_data_limit(key_id)
        return res.code == 204

    async def get_server_info(self):
        result = await self.api.get_server_info()

        data = result.json
        return ServerInfo(
            name=data['name'],
            server_id=data['serverId'],
            metrics_enabled=data['metricsEnabled'],
            created_at=data['createdTimestampMs'],
            version=data['version'],
            port=data['portForNewAccessKeys'],
            host=data['hostnameForAccessKeys'],
        )

    async def set_server_name(self, name: str) -> bool:
        res = await self.api.set_server_name(name=name)
        return res.code == 204

    async def set_hostname(self, hostname: str) -> bool:
        res = await self.api.set_hostname(hostname=hostname)
        return res.code == 204

    async def get_metrics_status(self) -> bool:
        res = await self.api.get_metrics_status()
        return res.json['metricsEnabled']

    async def set_metrics_status(self, status: bool) -> bool:
        res = await self.api.set_metrics_status(status=status)
        return res.code == 204

    async def set_port_new_for_access_keys(self, port: int) -> bool:
        res = await self.api.set_port_new_for_access_keys(port=port)
        return res.code == 204

    async def set_data_limit_for_all_keys(self, limit_bytes: int) -> bool:
        res = await self.api.set_data_limit_for_all_keys(limit_bytes=limit_bytes)
        return res.code == 204

    async def delete_data_limit_for_all_keys(self) -> bool:
        res = await self.api.delete_data_limit_for_all_keys()
        return res.code == 204
