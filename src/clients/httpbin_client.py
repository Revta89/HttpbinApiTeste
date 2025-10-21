from __future__ import annotations
import base64
import requests
from typing import Dict
from src.clients.base_client import BaseClient


class HttpBinClient(BaseClient):
    def __init__(self, base_url, timeout):
        super().__init__(base_url=base_url, timeout_seconds=timeout)

    # Response formats
    def get_json(self) -> requests.Response:
        return self.get("json")

    def get_html(self) -> requests.Response:
        return self.get("html")

    def get_robots_txt(self) -> requests.Response:
        return self.get("robots.txt")

    def get_xml(self) -> requests.Response:
        return self.get("xml")

    def get_ip_adress(self) -> requests.Response:
        return self.get(path="ip")

    def get_bytes(self, size: int) -> requests.Response:
        return self.get(f"bytes/{size}")

    def get_base_64(self, original_string: str) -> requests.Response:
        encoded_string = base64.b64encode(original_string.encode('utf-8')).decode('utf-8')
        return self.get(f"base64/{encoded_string}")

    # Request inspection
    def anything(self, path: str = "") -> requests.Response:
        if path:
            return self.get(f"anything/{path}")
        return self.get("anything")

    def headers(self, headers: Dict[str, str] | None = None) -> requests.Response:
        headers = headers or {}
        return self.get("headers", headers=headers)

    # Dynamic data helpers
    def uuid(self) -> requests.Response:
        return self.get("uuid")

    def get_delay(self, seconds: int) -> requests.Response:
        return self.get(f"delay/{seconds}")

    def post_delay(self, seconds: int) -> requests.Response:
        return self.post(f"delay/{seconds}")

    def update_delay(self, seconds: int) -> requests.Response:
        return self.put(f"delay/{seconds}")

    def delete_delay(self, seconds: int) -> requests.Response:
        return self.delete(f"delay/{seconds}")

