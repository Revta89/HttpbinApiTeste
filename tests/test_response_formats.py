import pytest
import allure
import json

pytestmark = pytest.mark.response_formats


@allure.story("JSON Response")
@allure.title("Verify JSON response format")
def test_json_response(httpbin_client):
    """Test endpoint that returns JSON response"""
    with allure.step("Send GET request to /json"):
        response = httpbin_client.get_json()
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify response content type"):
        assert "application/json" in response.headers.get("content-type", "")
    with allure.step("Verify JSON structure"):
        httpbin_client.validate_schema_file(response, "get_json.json")
        allure.attach(json.dumps(response.json(), indent=2), name="JSON Response",
                      attachment_type=allure.attachment_type.JSON)


@allure.story("XML Response")
@allure.title("Verify XML response format")
def test_xml_response(httpbin_client):
    """Test endpoint that returns XML response"""
    with allure.step("Send GET request to /xml"):
        response = httpbin_client.get_xml()
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify response content type"):
        assert "application/xml" in response.headers.get("content-type", "")
    with allure.step("Verify XML content"):
        assert "<?xml" in response.text


@allure.story("HTML Response")
@allure.title("Verify HTML response format")
def test_html_response(httpbin_client):
    """Test endpoint that returns HTML response"""
    with allure.step("Send GET request to /html"):
        response = httpbin_client.get_html()
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify response content type"):
        assert "text/html" in response.headers.get("content-type", "")
    with allure.step("Verify HTML content"):
        assert "<html>" in response.text
        assert "<body>" in response.text


@allure.story("Robots.txt")
@allure.title("Verify robots.txt response")
def test_robots_txt_response(httpbin_client):
    """Test robots.txt endpoint"""
    with allure.step("Send GET request to /robots.txt"):
        response = httpbin_client.get_robots_txt()
    with allure.step("Verify response status code"):
        httpbin_client.assert_response_code(response, 200)
    with allure.step("Verify response content type"):
        assert "text/plain" in response.headers.get("content-type", "")
    with allure.step("Verify robots.txt content"):
        assert "User-agent" in response.text
        assert "Disallow" in response.text

