from aio_clients import Http, Options
from aio_clients.multipart import Form, Easy


class OutlineClient:
    def __init__(self, *, url: str, cert_sha256: str = None):
        self.http = Http(
            host=url,
            option=Options(
                is_ssl=None,
                request_kwargs={'fingerprint': bytes.fromhex(cert_sha256)}
            ))

    async def metrics_transfer(self):
        return await self.http.get('metrics/transfer')

    async def get_keys(self):
        return await self.http.get('access-keys/')

    async def create_key(self):
        return await self.http.get('access-keys/')

    async def rename_key(self, key_id: int, name: str):
        with Easy('form-data') as form:
            form.add_form(Form(key='name', value=name))

        return await self.http.put(
            f'access-keys/{key_id}/name',
            form=form,
            o=Options(is_json=False),
        )

    async def delete_key(self, key_id: int):
        return await self.http.delete(f'access-keys/{key_id}')

    async def add_data_limit(self, key_id: int, limit_bytes: int):
        return await self.http.put(
            f'access-keys/{key_id}/data-limit',
            json={'limit': {"limit": {"bytes": limit_bytes}}}
        )

    async def delete_data_limit(self, key_id: int):
        return await self.http.delete(
            f'access-keys/{key_id}/data-limit',
            o=Options(is_json=False),
        )

    async def get_transferred_data(self):
        return await self.http.get('metrics/transfer')

    async def get_server_information(self):
        return await self.http.get('server')

    async def set_server_name(self, name: str):
        return await self.http.put(
            'server/name',
            json={'name': name}
        )

    async def set_hostname(self, hostname: str):
        return await self.http.put(
            "server/hostname-for-access-keys",
            json={"hostname": hostname}
        )

    async def get_metrics_status(self):
        return await self.http.get("metrics/enabled")

    async def set_metrics_status(self, status: bool):
        return await self.http.put(
            "/metrics/enabled",
            json={"metricsEnabled": status}
        )

    async def set_port_new_for_access_keys(self, port: int):
        return await self.http.put(
            "server/port-for-new-access-keys",
            json={"port": port}
        )

    async def set_data_limit_for_all_keys(self, limit_bytes: int):
        return await self.http.put(
            "server/access-key-data-limit",
            json={"limit": {"bytes": limit_bytes}}
        )

    async def delete_data_limit_for_all_keys(self):
        return await self.http.delete("server/access-key-data-limit")
