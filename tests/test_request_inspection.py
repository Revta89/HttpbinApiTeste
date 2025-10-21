import pytest
import allure

pytestmark = pytest.mark.request_inspection


@allure.story("Headers Inspection")
@allure.title("Verify request headers are returned correctly")
def test_headers_inspection(httpbin_client, generator):
    """Test that request headers are properly returned"""
    custom_headers = generator.generate_headers()
    with allure.step("Send GET request with custom headers"):
        response = httpbin_client.headers(headers=custom_headers)
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify headers in response"):
        header_keys_lower = {k.lower(): v for k, v in response.json()["headers"].items()}
        assert "x-test-run" in header_keys_lower


@allure.story("IP Address Inspection")
@allure.title("Verify IP address is returned correctly")
def test_ip_inspection(httpbin_client):
    """Test IP address inspection endpoint"""
    with allure.step("Send GET request to /ip"):
        response = httpbin_client.get_ip_adress()
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify IP address in response"):
        data = response.json()
        assert "origin" in data
        assert "." in data["origin"] or ":" in data["origin"]


@allure.story("User Agent Inspection")
@allure.title("Verify user agent is returned correctly")
def test_user_agent_inspection(httpbin_client):
    """Test user agent inspection endpoint"""
    custom_user_agent = "Custom-Test-Agent/1.0"
    with allure.step("Send GET request with custom user agent"):
        response = httpbin_client.get("/user-agent", headers={"User-Agent": custom_user_agent})
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify user agent in response"):
        data = response.json()
        assert data["user-agent"] == custom_user_agent


@allure.story("Request Method Inspection")
@allure.title("Verify different HTTP methods work correctly")
@pytest.mark.parametrize("method", ["GET", "POST", "PUT", "DELETE"])
def test_request_methods(httpbin_client, method, generator):
    """Test different HTTP methods"""
    test_data = {"test_data": generator.generate_random_string()}
    with allure.step(f"Send {method} request to /{method.lower()}"):
        if method == "GET":
            response = httpbin_client.get(path=f"/{method.lower()}")
        elif method == "POST":
            response = httpbin_client.post(path=f"/{method.lower()}", data=test_data)
        elif method == "PUT":
            response = httpbin_client.put(f"/{method.lower()}", data=test_data)
        elif method == "DELETE":
            response = httpbin_client.delete(f"/{method.lower()}")
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify method in response"):
        data = response.json()
        if "method" in data:
            assert data["method"] == method.upper()
