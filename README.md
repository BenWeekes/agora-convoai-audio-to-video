# Agora ConvoAI Audio-to-Video Integration

This repository provides a generic protocol and implementation for external services to receive audio output from Agora's ConvoAI platform, enabling real-time generation and publishing of audio and video content back into Agora channels. This creates interactive experiences such as AI-powered avatars, interactive movies, and other real-time multimedia applications.

## Overview

The integration follows a three-phase workflow:

1. **Connection Setup** - Establish session and obtain WebSocket connection details
2. **Audio Streaming** - Receive real-time audio data from ConvoAI via WebSocket
3. **Video Publishing** - Generate and publish audio/video content back to Agora channel

## Architecture Flow

![Agora ConvoAI Integration Sequence Diagram](sequence-diagram.svg)

## Implementation Components

### 1. Connection Setup API
[📁 connection-setup/](./connection-setup/)

### 2. WebSocket Audio Streaming
[📁 websocket-receive-audio/](./websocket-receive-audio/)

### 3. Go Audio/Video Publishing
[📁 go-publish-audio-video/](./go-publish-audio-video/)