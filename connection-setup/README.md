# Connection Setup API Documentation

This document describes the REST API endpoint you should create for establishing video generation sessions and providing WebSocket connection details to Agora convoAI platform.

## Example Endpoint

```
POST /session/start
```

## Headers

```json
{
  "accept": "application/json",
  "content-type": "application/json"
}
```

## Request Format

```json
{
  "api_key": "YOUR_API_KEY",
  "avatar_id": "16cb73e7de08",
  "quality": "high",
  "version": "v1",
  "video_encoding": "H264",
  "agora_settings": {
    "app_id": "dllkSlkdmmppollalepls",
    "token": "lkmmopplek",
    "channel": "room1",
    "uid": "333",
    "enable_string_uid": false
  }
}
```

## Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| api_key | string | Yes | API authentication key for accessing the service |
| avatar_id | string | Yes | Unique identifier for the avatar to be used in the session. This ID determines which virtual avatar will be rendered and animated during the video stream. |
| quality | string | Yes | Video quality setting for the avatar stream. Accepted values: `"low"`, `"medium"`, `"high"`. Higher quality settings provide better visual fidelity but require more bandwidth. |
| version | string | Yes | API version identifier. Currently supports `"v1"`. This ensures compatibility between client and server implementations. |
| video_encoding | string | Yes | Video codec to be used for encoding the avatar stream. Supported values: `"H264"`, `"VP8"`, `"AV1"`. H264 provides the widest compatibility across devices and browsers. |
| agora_settings | object | Yes | Configuration object for Agora RTC (Real-Time Communication) integration. Contains all necessary parameters for establishing the video/audio channel. |

### Agora Settings Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| app_id | string | Yes | Agora application identifier. |
| token | string | Yes | Agora authentication token for secure channel access. |
| channel | string | Yes | Name of the Agora channel to join. |
| uid | string | Yes | User ID within the Agora channel. |
| enable_string_uid | boolean | Yes | Determines whether the uid field should be treated as a string or numeric value. |

## Response Format

### Success Response (200 OK)

```json
{
  "websocket_address": "wss://api.example.com/v1/websocket",
  "session_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| websocket_address | string | WebSocket URL to connect to for audio streaming. Use this address to establish the WebSocket connection. |
| session_token | string | JWT token for WebSocket authentication. Include this in the WebSocket connection headers as `Authorization: Bearer {session_token}`. |

### Error Response (400 Bad Request)

```json
{
  "error": "Invalid request",
  "message": "Missing required field: avatar_id",
  "code": "VALIDATION_ERROR"
}
```

### Error Response (401 Unauthorized)

```json
{
  "error": "Unauthorized", 
  "message": "Invalid API key",
  "code": "INVALID_API_KEY"
}
```

## Usage Flow

1. **Send POST request** to `/v1/sessions` with session configuration and API key
2. **Receive response** containing `websocket_address` and `session_token`
3. **Connect to WebSocket** using the provided address and token
4. **Send init command** via WebSocket with the same configuration (excluding api_key)
5. **Stream audio data** using voice commands

## Testing

Use the provided test script to verify the endpoint:

```bash
python endpoint_post.py
```