import os
import yaml
from dataclasses import dataclass
from typing import Any, Dict
from dotenv import load_dotenv


@dataclass()
class RetryConfig:
    max_attempts: int
    backoff_seconds: float


@dataclass()
class HttpConfig:
    timeout_seconds: int


@dataclass()
class AppConfig:
    base_url: str
    http: HttpConfig
    retry: RetryConfig
    allure_dir: str


class Config:
    def __init__(self, yaml_path: str = os.path.join(os.path.dirname(__file__), 'config.yaml'),
                 env_file: str = ".env") -> None:
        load_dotenv(env_file)
        self._yaml_path = yaml_path

    def load(self) -> AppConfig:
        with open(self._yaml_path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = yaml.safe_load(f) or {}

        base_url = os.getenv("HTTPBIN_BASE_URL", data.get("httpbin", {}).get("base_url", "https://httpbin.org"))
        timeout_seconds = int(os.getenv("HTTP_TIMEOUT", data.get("http", {}).get("timeout_seconds", 10)))
        max_attempts = int(os.getenv("RETRY_MAX_ATTEMPTS", data.get("retry", {}).get("max_attempts", 5)))
        backoff_seconds = float(os.getenv("RETRY_BACKOFF_SECONDS", data.get("retry", {}).get("backoff_seconds", 0.5)))
        allure_dir = data.get("reporting", {}).get("allure_dir", "reports/allure")

        return AppConfig(
            base_url=base_url,
            http=HttpConfig(timeout_seconds=timeout_seconds),
            retry=RetryConfig(max_attempts=max_attempts, backoff_seconds=backoff_seconds),
            allure_dir=allure_dir,
        )


config = Config()