from aio_clients import Http, Options, Response
from aio_clients.multipart import Form, Easy


class Client:
    def __init__(self, *, url: str, cert_sha256: str):
        self.http = Http(
            host=url,
            option=Options(
                is_ssl=None,
                request_kwargs={
                    'fingerprint': bytes.fromhex(cert_sha256),
                    'raise_for_status': True
                },
            ),
        )

    async def metrics_transfer(self) -> Response:
        return await self.http.get('metrics/transfer')

    async def get_keys(self) -> Response:
        return await self.http.get('access-keys/')

    async def create_key(self) -> Response:
        return await self.http.post('access-keys/')

    async def rename_key(self, key_id: str, name: str) -> Response:
        with Easy('form-data') as form:
            form.add_form(Form(key='name', value=name))

        return await self.http.put(
            f'access-keys/{key_id}/name',
            form=form,
            o=Options(is_json=False),
        )

    async def delete_key(self, key_id: str) -> Response:
        return await self.http.delete(
            f'access-keys/{key_id}',
            o=Options(is_json=False),
        )

    async def set_data_limit(self, key_id: str, limit_bytes: int) -> Response:
        return await self.http.put(
            f'access-keys/{key_id}/data-limit',
            json={'limit': {"limit": {"bytes": limit_bytes}}},
            o=Options(is_json=False),
        )

    async def delete_data_limit(self, key_id: str) -> Response:
        return await self.http.delete(
            f'access-keys/{key_id}/data-limit',
            o=Options(is_json=False),
        )

    async def get_server_info(self) -> Response:
        return await self.http.get('server')

    async def set_server_name(self, name: str) -> Response:
        return await self.http.put(
            'server/name',
            json={'name': name},
            o=Options(is_json=False),
        )

    async def set_hostname(self, hostname: str) -> Response:
        return await self.http.put(
            "server/hostname-for-access-keys",
            json={"hostname": hostname},
            o=Options(is_json=False),
        )

    async def get_metrics_status(self) -> Response:
        return await self.http.get("metrics/enabled")

    async def set_metrics_status(self, status: bool) -> Response:
        return await self.http.put(
            "/metrics/enabled",
            json={"metricsEnabled": status},
            o=Options(is_json=False),
        )

    async def set_port_new_for_access_keys(self, port: int) -> Response:
        return await self.http.put(
            "server/port-for-new-access-keys",
            json={"port": port},
            o=Options(is_json=False),
        )

    async def set_data_limit_for_all_keys(self, limit_bytes: int) -> Response:
        return await self.http.put(
            "server/access-key-data-limit",
            json={"limit": {"bytes": limit_bytes}},
            o=Options(is_json=False),
        )

    async def delete_data_limit_for_all_keys(self) -> Response:
        return await self.http.delete(
            "server/access-key-data-limit",
            o=Options(is_json=False),
        )
