from src.clients.httpbin_client import HttpBinClient
import pytest
import allure
import json
from src.utils.data_factory import data_generator
from config.config import Config


@pytest.fixture(scope="session")
def app_config():
    """Load config once per session"""
    return Config().load()


@pytest.fixture(scope="session")
def httpbin_client(app_config):
    """Provide API client instance"""
    return HttpBinClient(app_config.base_url, app_config.http.timeout_seconds)


@pytest.fixture
def generator():
    """Provide data generator instance"""
    return data_generator


@pytest.fixture(autouse=True)
def attach_test_info(request):
    """Attach test information to Allure reports"""
    yield
    # add custom attachments after test execution
    if hasattr(request.node, 'rep_call') and request.node.rep_call.passed:
        # add test metadata to report
        with allure.step("Test Metadata"):
            allure.attach(
                json.dumps({
                    "test_name": request.node.name,
                    "module": request.node.module.__name__,
                }, indent=2),
                name="Test Information",
                attachment_type=allure.attachment_type.JSON
            )