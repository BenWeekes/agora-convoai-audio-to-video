#!/usr/bin/env python3
"""
Mock server for testing session start/stop endpoints.
Listens on port 8764 and provides mock responses for testing.
"""

import json
import logging
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import uuid

# Configuration
SERVER_PORT = 8764
WEBSOCKET_ADDRESS = "ws://localhost:8765"
VALID_API_KEY = "YOUR_API_KEY"

# In-memory storage for active sessions
active_sessions = {}

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SessionHandler(BaseHTTPRequestHandler):
    """HTTP request handler for session management endpoints"""
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(f"{self.address_string()} - {format % args}")
    
    def _send_json_response(self, status_code, data):
        """Send JSON response with proper headers"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, x-api-key, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def _get_request_body(self):
        """Parse JSON request body"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                return json.loads(body.decode('utf-8'))
            return {}
        except Exception as e:
            logger.error(f"Error parsing request body: {e}")
            return None
    
    def _validate_api_key(self):
        """Validate API key from headers"""
        api_key = self.headers.get('x-api-key')
        
        if not api_key:
            self._send_json_response(403, {
                "error": "Forbidden",
                "message": "API key header missing",
                "code": "MISSING_API_KEY"
            })
            return False
        
        if api_key != VALID_API_KEY:
            self._send_json_response(401, {
                "error": "Unauthorized",
                "message": "Invalid API key",
                "code": "INVALID_API_KEY"
            })
            return False
        
        return True
    
    def _generate_session_token(self):
        """Generate a mock JWT session token"""
        # This is a mock token for testing purposes
        header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        payload_data = {
            "sub": str(uuid.uuid4()),
            "exp": int(time.time()) + 3600,  # 1 hour from now
            "iat": int(time.time()),
            "session_id": str(uuid.uuid4())
        }
        payload = json.dumps(payload_data, separators=(',', ':'))
        # Base64 encode the payload (simplified for testing)
        import base64
        payload_b64 = base64.b64encode(payload.encode()).decode().rstrip('=')
        signature = "test_signature_for_mock_server"
        
        return f"{header}.{payload_b64}.{signature}"
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self._send_json_response(200, {})
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        logger.info(f"POST {self.path}")
        logger.info(f"Headers: {dict(self.headers)}")
        
        if parsed_path.path == '/session/start':
            self.handle_session_start()
        else:
            self._send_json_response(404, {
                "error": "Not Found",
                "message": f"Endpoint not found: {self.path}",
                "code": "ENDPOINT_NOT_FOUND"
            })
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        parsed_path = urlparse(self.path)
        
        logger.info(f"DELETE {self.path}")
        logger.info(f"Headers: {dict(self.headers)}")
        
        if parsed_path.path == '/session/stop':
            self.handle_session_stop()
        else:
            self._send_json_response(404, {
                "error": "Not Found",
                "message": f"Endpoint not found: {self.path}",
                "code": "ENDPOINT_NOT_FOUND"
            })
    
    def handle_session_start(self):
        """Handle session start POST request"""
        logger.info("Handling session start request")
        
        # Validate API key
        if not self._validate_api_key():
            return
        
        # Parse request body
        request_data = self._get_request_body()
        if request_data is None:
            self._send_json_response(400, {
                "error": "Invalid request",
                "message": "Invalid JSON in request body",
                "code": "INVALID_JSON"
            })
            return
        
        logger.info(f"Request data: {json.dumps(request_data, indent=2)}")
        
        # Validate required fields
        required_fields = ["avatar_id", "quality", "version", "video_encoding", "agora_settings"]
        missing_fields = []
        
        for field in required_fields:
            if field not in request_data:
                missing_fields.append(field)
        
        if missing_fields:
            self._send_json_response(400, {
                "error": "Invalid request",
                "message": f"Missing required field(s): {', '.join(missing_fields)}",
                "code": "VALIDATION_ERROR"
            })
            return
        
        # Validate agora_settings structure
        agora_settings = request_data.get("agora_settings", {})
        required_agora_fields = ["app_id", "token", "channel", "uid", "enable_string_uid"]
        missing_agora_fields = []
        
        for field in required_agora_fields:
            if field not in agora_settings:
                missing_agora_fields.append(field)
        
        if missing_agora_fields:
            self._send_json_response(400, {
                "error": "Invalid request",
                "message": f"Missing required agora_settings field(s): {', '.join(missing_agora_fields)}",
                "code": "VALIDATION_ERROR"
            })
            return
        
        # Validate quality values
        valid_qualities = ["low", "medium", "high"]
        if request_data["quality"] not in valid_qualities:
            self._send_json_response(400, {
                "error": "Invalid request",
                "message": f"Invalid quality value. Must be one of: {', '.join(valid_qualities)}",
                "code": "VALIDATION_ERROR"
            })
            return
        
        # Validate video encoding values
        valid_encodings = ["H264", "VP8", "AV1"]
        if request_data["video_encoding"] not in valid_encodings:
            self._send_json_response(400, {
                "error": "Invalid request",
                "message": f"Invalid video_encoding value. Must be one of: {', '.join(valid_encodings)}",
                "code": "VALIDATION_ERROR"
            })
            return
        
        # Generate session token and store session
        session_token = self._generate_session_token()
        session_data = {
            "created_at": time.time(),
            "avatar_id": request_data["avatar_id"],
            "quality": request_data["quality"],
            "status": "active"
        }
        active_sessions[session_token] = session_data
        
        logger.info(f"Created new session with token: {session_token[:20]}...")
        logger.info(f"Active sessions count: {len(active_sessions)}")
        
        # Return success response
        response_data = {
            "websocket_address": WEBSOCKET_ADDRESS,
            "session_token": session_token
        }
        
        logger.info(f"Sending success response: {json.dumps(response_data, indent=2)}")
        self._send_json_response(200, response_data)
    
    def handle_session_stop(self):
        """Handle session stop DELETE request"""
        logger.info("Handling session stop request")
        
        # Validate API key
        if not self._validate_api_key():
            return
        
        # Parse request body
        request_data = self._get_request_body()
        if request_data is None:
            self._send_json_response(400, {
                "error": "Invalid request",
                "message": "Invalid JSON in request body",
                "code": "INVALID_JSON"
            })
            return
        
        logger.info(f"Request data: {json.dumps(request_data, indent=2)}")
        
        # Validate required fields
        session_token = request_data.get("session_token")
        if not session_token:
            self._send_json_response(400, {
                "error": "Invalid request",
                "message": "Missing required field: session_token",
                "code": "VALIDATION_ERROR"
            })
            return
        
        # Check if session exists
        if session_token not in active_sessions:
            self._send_json_response(404, {
                "error": "Not found",
                "message": "Session not found or already terminated",
                "code": "SESSION_NOT_FOUND"
            })
            return
        
        # Remove session from active sessions
        del active_sessions[session_token]
        logger.info(f"Terminated session with token: {session_token[:20]}...")
        logger.info(f"Active sessions count: {len(active_sessions)}")
        
        # Return success response
        response_data = {
            "status": "success",
            "message": "Session terminated successfully"
        }
        
        logger.info(f"Sending success response: {json.dumps(response_data, indent=2)}")
        self._send_json_response(200, response_data)


def main():
    """Start the mock server"""
    logger.info("=" * 60)
    logger.info("SESSION TEST RECEIVER SERVER")
    logger.info("=" * 60)
    logger.info(f"Starting mock server on port {SERVER_PORT}")
    logger.info(f"WebSocket address will be: {WEBSOCKET_ADDRESS}")
    logger.info(f"Valid API key: {VALID_API_KEY}")
    logger.info("")
    logger.info("Available endpoints:")
    logger.info(f"  POST   http://localhost:{SERVER_PORT}/session/start")
    logger.info(f"  DELETE http://localhost:{SERVER_PORT}/session/stop")
    logger.info("")
    logger.info("To test with your scripts, update the API_ENDPOINT to:")
    logger.info(f"  API_ENDPOINT = \"http://localhost:{SERVER_PORT}/session/start\"")
    logger.info(f"  API_ENDPOINT = \"http://localhost:{SERVER_PORT}/session/stop\"")
    logger.info("")
    logger.info("Press Ctrl+C to stop the server")
    logger.info("=" * 60)
    
    # Create and start server
    try:
        server_address = ('localhost', SERVER_PORT)
        httpd = HTTPServer(server_address, SessionHandler)
        
        logger.info(f"✅ Server started successfully on http://localhost:{SERVER_PORT}")
        logger.info("Waiting for requests...")
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Server shutdown requested")
        httpd.shutdown()
        logger.info("✅ Server stopped")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        raise


if __name__ == "__main__":
    main()
