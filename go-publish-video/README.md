# Agora Go SDK Setup Guide

This guide walks you through setting up the Agora Go SDK on Linux for audio/video publishing capabilities as part of the Agora ConvoAI Audio-to-Video Integration system.

## Prerequisites

- Linux system (Ubuntu/Debian recommended)
- sudo privileges
- Internet connection

## Installation Steps

### 1. Install Build Essentials and Go

```bash
# Update package manager
sudo apt-get update

# Install required build tools
sudo apt-get install -y build-essential git wget

# Download and install Go 1.21
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz

# Add Go to PATH
export PATH=$PATH:/usr/local/go/bin

# Install FlatBuffers compiler
sudo apt-get install -y flatbuffers-compiler
```

### 2. Download Agora SDK

```bash
# Create directory for Agora SDK
mkdir -p ~/agora-sdk && cd ~/agora-sdk

# Download Agora RTC SDK
wget https://download.agora.io/rtsasdk/release/Agora-RTC-x86_64-linux-gnu-v4.4.32-20250425_144419-675648.tgz

# Extract the SDK
tar -xzf Agora-RTC-x86_64-linux-gnu-v4.4.32-20250425_144419-675648.tgz
```

### 3. Setup Agora Go SDK

```bash
# Clone the Agora Golang Server SDK
cd ~
git clone https://github.com/AgoraIO-Extensions/Agora-Golang-Server-SDK.git
cd Agora-Golang-Server-SDK

# Checkout specific version
git checkout v2.1.0

# Backup problematic file
mv go_sdk/agoraservice/audio_vad.go go_sdk/agoraservice/audio_vad.go.bak
```

### 4. Configure Environment Variables

```bash
# Set Agora SDK path
export AGORA_SDK_PATH=~/agora-sdk/agora_rtc_sdk/agora_sdk

# Configure CGO flags for compilation
export CGO_CFLAGS="-I$AGORA_SDK_PATH/include -I$AGORA_SDK_PATH/include/c -I$AGORA_SDK_PATH/include/c/base -I$AGORA_SDK_PATH/include/c/api2 -I$AGORA_SDK_PATH/include/api/cpp -I$AGORA_SDK_PATH/include/c/rte/rte_base/c"
export CGO_LDFLAGS="-L$AGORA_SDK_PATH -lagora_rtc_sdk"

# Set library path
export LD_LIBRARY_PATH="$AGORA_SDK_PATH:$LD_LIBRARY_PATH"
```

### 5. Build and Run

```bash
# Navigate to the audio/video publishing example
cd go-publish-audio-video

# Clean and build the project
make clean
make build

# Run the application (replace with your actual values)
./parent -appID "your_agora_app_id" -channelName "your_channel" -enableStringUID=false -userID "your_user_id"
```

## Configuration

Before running the application, make sure to replace the following placeholders with your actual Agora credentials:

- `your_agora_app_id`: Your Agora App ID from the Agora Console
- `your_channel`: The channel name you want to join
- `your_user_id`: Your user ID for the session

## Troubleshooting

- Ensure all environment variables are properly set
- Verify that the Agora SDK path is correct
- Check that all dependencies are installed
- Make sure you have the correct permissions for the directories

## Notes

- This setup uses Go 1.21.5 and Agora SDK v4.4.32
- The `audio_vad.go` file is backed up due to potential compilation issues
- Environment variables need to be set each time you start a new terminal session
