# Agora ConvoAI Audio-to-Video Integration

This repository provides a generic protocol and implementation for external services to receive audio output from Agora's ConvoAI platform, enabling real-time generation and publishing of audio and video content back into Agora channels. This creates interactive experiences such as AI-powered avatars, interactive movies, and other real-time multimedia applications.

## Overview

The integration follows a three-phase workflow:

1. **Connection Setup** - Establish session and obtain WebSocket connection details
2. **Audio Streaming** - Receive real-time audio data from ConvoAI via WebSocket
3. **Video Publishing** - Generate and publish audio/video content back to Agora channel

## Architecture Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agora ConvoAI │    │ Avatar Provider │    │ Avatar Provider │    │  Agora Channel  │
│                 │    │ (Main Domain)   │    │  (WebSocket)    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │                       │                       │
          │                       │                       │                       │
          │  Initial Connection Setup                     │                       │
          │                       │                       │                       │
          │ POST /endpoint        │                       │                       │
          │ {region, api_key,     │                       │                       │
          │  avatar_id,           │                       │                       │
          │  agora_token,         │                       │                       │
          │  agora_uid,           │                       │                       │
          │  agora_channel}       │                       │                       │
          │──────────────────────▶│                       │                       │
          │                       │                       │                       │
          │        Response       │                       │                       │
          │ {session_id,          │                       │                       │
          │  websocket_address}   │                       │                       │
          │◀──────────────────────│                       │                       │
          │                       │                       │                       │
          │                WebSocket Connection           │                       │
          │                       │                       │                       │
          │       Connect to websocket_address            │                       │
          │       {session_id, avatar_id,                 │                       │
          │        agora_token, agora_uid, agora_channel} │                       │
          │───────────────────────────────────────────────▶│                       │
          │                       │                       │                       │
          │              Connection Established           │                       │
          │◀───────────────────────────────────────────────│                       │
          │                       │                       │                       │
          │                       │          Avatar Publishing                    │
          │                       │                       │                       │
          │                       │        Publish Avatar Audio/Video           │
          │                       │        (via Golang SDK)                      │
          │                       │───────────────────────────────────────────────▶│
          │                       │                       │                       │
          │                       │           Ongoing Call Metrics               │
          │                       │◀───────────────────────────────────────────────│
          │                       │                       │                       │
          │             Ongoing Communication             │                       │
          │                       │                       │                       │
          │ ┌─────────────────────┐│      [Interaction Loop]                      │
          │ │      Loop           ││                       │                       │
          │ │                     ││                       │                       │
          │ │ alt ─────────────── ││      [Voice Command]  │                       │
          │ │                     ││                       │                       │
          │ │                     ││ {command: "voice",    │                       │
          │ │     audio: "base64_encoded_audio",            │                       │
          │ │     sampleRate: 24000,                       │                       │
          │ │     encoding: "PCM16"}                       │                       │
          │ │ ────────────────────────────────────────────▶│                       │
          │ │                     ││                       │                       │
          │ │          [State Command]                     │                       │
          │ │                     ││                       │                       │
          │ │ {command: "state", value: "listen" │ "talk" │ "idle"}              │
          │ │ ────────────────────────────────────────────▶│                       │
          │ │                     ││                       │                       │
          │ │         [Special Command]                    │                       │
          │ │                     ││                       │                       │
          │ │ {command: "special",                         │                       │
          │ │  content: "XML markup for avatar gestures"} │                       │
          │ │ ────────────────────────────────────────────▶│ Process Command &    │
          │ │                     ││                       │ Update Avatar        │
          │ │                     ││                       │                       │
          │ │                     ││                       │         ┌─────────┐  │
          │ │                     ││                       │         │         │  │
          │ │                     ││                       │         └─────────┘  │
          │ │                     ││                       │                       │
          │ │                     ││                       │    Update Avatar     │
          │ │                     ││                       │  Audio/Video Stream  │
          │ │                     ││                       │───────────────────────▶│
          │ └─────────────────────┘│                       │                       │
          │                       │                       │                       │
          │                       │                       │                       │
Avatar states can switch between idle and listening based on commands
```

## Implementation Components

### 1. Connection Setup API
[📁 connection-setup/](./connection-setup/)

### 2. WebSocket Audio Streaming
[📁 websocket-receive-audio/](./websocket-receive-audio/)

### 3. Go Audio/Video Publishing
[📁 go-publish-audio-video/](./go-publish-audio-video/)