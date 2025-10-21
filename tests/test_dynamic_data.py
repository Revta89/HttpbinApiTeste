import pytest
from src.utils.retry import retry
import allure

pytestmark = pytest.mark.dynamic_data


@allure.story("UUID Generation")
@allure.title("Verify UUID generation")
def test_uuid_generation(httpbin_client):
    """Test UUID generation endpoint"""
    with allure.step("Send GET request to /uuid"):
        response = httpbin_client.uuid()
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify UUID in response"):
        data = response.json()
        length = len(data["uuid"])
        assert "uuid" in data, "UUID is not present in response"
        assert length == 36, f"Expected length {length} UUID"


@allure.story("Base64 Encoding")
@allure.title("Verify base64 encoding/decoding")
def test_base64_encoding(httpbin_client, generator):
    """Test base64 encoding endpoint"""
    original_string = generator.generate_random_string()
    with allure.step(f"Encode string: {original_string}"):
        response = httpbin_client.get_base_64(original_string)
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify encoded content"):
        assert response.text == original_string


@allure.story("Bytes Generation")
@allure.title("Verify random bytes generation")
@pytest.mark.parametrize("size", [10, 100, 500])
def test_bytes_generation(httpbin_client, size):
    """Test random bytes generation with different sizes"""
    with allure.step(f"Request {size} bytes"):
        response = httpbin_client.get_bytes(size)
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify response content length"):
        assert len(response.content) == size


@allure.story("Delay Simulation")
@allure.title("Verify delayed response")
@pytest.mark.slow
def test_delayed_response(httpbin_client, app_config, delay_seconds=2):
    """Test delayed response endpoint"""
    with allure.step(f"Request with {delay_seconds} seconds delay"):
        @retry(app_config.retry.max_attempts, app_config.retry.backoff_seconds)
        def call():
            return httpbin_client.get_delay(delay_seconds)
        response = call()
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify response contains expected data"):
        data = response.json()
        assert f"delay/{delay_seconds}" in data["url"]


@allure.story("JSON Data Validation")
@allure.title("Verify JSON data validation with dynamic data")
def test_json_validation(httpbin_client, generator):
    """Test JSON validation with dynamically generated data"""
    test_data = generator.generate_json_payload()
    with allure.step("Send POST request with generated JSON data"):
        response = httpbin_client.post("/anything", payload=test_data)
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify returned JSON data"):
        response_data = response.json()
        assert "json" in response_data
        assert response_data["json"] == test_data
