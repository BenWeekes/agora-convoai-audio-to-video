import requests
import json
import logging

# Configuration
API_ENDPOINT = "https://api.example.com/v1/sessions"  # Update with actual endpoint
# API_ENDPOINT = "http://localhost:8080/v1/sessions"  # For local testing
API_KEY = "YOUR_API_KEY"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_connection_setup_endpoint():
    """Test the connection setup POST endpoint"""
    
    # Prepare test payload
    payload = {
        "api_key": API_KEY,
        "avatar_id": "16cb73e7de08",
        "quality": "high",
        "version": "v1",
        "video_encoding": "H264",
        "agora_settings": {
            "app_id": "dllkSlkdmmppollalepls",
            "token": "lkmmopplek",
            "channel": "room1",
            "uid": "333",
            "enable_string_uid": False
        }
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    
    logger.info(f"Testing endpoint: {API_ENDPOINT}")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Send POST request
        response = requests.post(
            API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
        
        # Parse response
        if response.headers.get('content-type', '').startswith('application/json'):
            response_data = response.json()
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
        else:
            logger.info(f"Response text: {response.text}")
            response_data = {}
        
        # Verify successful response
        if response.status_code == 200:
            logger.info("✅ Request successful!")
            return verify_success_response(response_data)
        else:
            logger.error(f"❌ Request failed with status {response.status_code}")
            return verify_error_response(response_data, response.status_code)
            
    except requests.exceptions.ConnectionError as e:
        logger.error(f"❌ Connection error: {e}")
        logger.error("Make sure the API endpoint is running and accessible")
        return False
    except requests.exceptions.Timeout as e:
        logger.error(f"❌ Request timeout: {e}")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Request error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False


def verify_success_response(data):
    """Verify that success response contains expected fields"""
    logger.info("Verifying success response structure...")
    
    required_fields = ["websocket_address", "session_token"]
    missing_fields = []
    
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        else:
            logger.info(f"✅ Found required field: {field}")
    
    if missing_fields:
        logger.error(f"❌ Missing required fields: {missing_fields}")
        return False
    
    # Verify websocket_address format
    websocket_address = data["websocket_address"]
    if not (websocket_address.startswith("ws://") or websocket_address.startswith("wss://")):
        logger.error(f"❌ Invalid websocket_address format: {websocket_address}")
        logger.error("Expected to start with 'ws://' or 'wss://'")
        return False
    else:
        logger.info(f"✅ Valid websocket_address format: {websocket_address}")
    
    # Verify session_token is not empty
    session_token = data["session_token"]
    if not session_token or len(session_token.strip()) == 0:
        logger.error("❌ session_token is empty")
        return False
    else:
        logger.info(f"✅ session_token present (length: {len(session_token)} chars)")
        # Log first and last few characters for debugging
        if len(session_token) > 20:
            logger.info(f"Token preview: {session_token[:10]}...{session_token[-10:]}")
    
    logger.info("✅ All response validation checks passed!")
    return True


def verify_error_response(data, status_code):
    """Verify that error response contains expected fields"""
    logger.info(f"Verifying error response structure for status {status_code}...")
    
    if not data:
        logger.warning("No response data received for error")
        return False
    
    # Check for common error fields
    error_fields = ["error", "message"]
    found_fields = []
    
    for field in error_fields:
        if field in data:
            found_fields.append(field)
            logger.info(f"✅ Found error field: {field} = {data[field]}")
    
    if not found_fields:
        logger.warning("❌ No standard error fields found in response")
        return False
    
    logger.info("✅ Error response structure is valid")
    return True


def test_invalid_api_key():
    """Test the endpoint with an invalid API key"""
    logger.info("\n" + "="*50)
    logger.info("Testing with invalid API key...")
    
    payload = {
        "api_key": "INVALID_API_KEY",
        "avatar_id": "test_avatar",
        "quality": "high",
        "version": "v1",
        "video_encoding": "H264",
        "agora_settings": {
            "app_id": "test_app_id",
            "token": "test_token",
            "channel": "test_channel",
            "uid": "123",
            "enable_string_uid": False
        }
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    
    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload, timeout=30)
        logger.info(f"Response status code: {response.status_code}")
        
        if response.status_code == 401:
            logger.info("✅ Correctly received 401 Unauthorized for invalid API key")
            return True
        else:
            logger.warning(f"⚠️ Expected 401 but got {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during invalid API key test: {e}")
        return False


def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("CONNECTION SETUP ENDPOINT TEST")
    logger.info("=" * 60)
    
    # Test 1: Valid request
    logger.info("\n" + "="*50)
    logger.info("Test 1: Valid API request")
    logger.info("="*50)
    
    success1 = test_connection_setup_endpoint()
    
    # Test 2: Invalid API key
    logger.info("\n" + "="*50)
    logger.info("Test 2: Invalid API key")
    logger.info("="*50)
    
    success2 = test_invalid_api_key()
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("TEST SUMMARY")
    logger.info("="*50)
    
    logger.info(f"Valid request test: {'✅ PASSED' if success1 else '❌ FAILED'}")
    logger.info(f"Invalid API key test: {'✅ PASSED' if success2 else '❌ FAILED'}")
    
    if success1 and success2:
        logger.info("🎉 All tests passed!")
    else:
        logger.info("⚠️ Some tests failed. Check the logs above for details.")


if __name__ == "__main__":
    main()
