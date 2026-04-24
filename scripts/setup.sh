#!/bin/bash
# scripts/setup.sh
# Install everything SignBridge needs
# Run: bash scripts/setup.sh

echo "=================================="
echo "  SignBridge — Setup"
echo "=================================="

# System packages
echo "[1] Installing system packages..."
sudo apt update -q
sudo apt install -y \
    python3-picamera2 \
    libcap-dev \
    espeak \
    git-lfs

# Python packages
echo "[2] Installing Python packages..."
source ~/sign_project/bin/activate
pip install \
    mediapipe \
    opencv-python-headless \
    scikit-learn==1.6.1 \
    joblib \
    gtts \
    pygame \
    requests \
    numpy==1.26.4 \
    arabic-reshaper \
    python-bidi \
    Pillow

# Link libcamera
echo "[3] Linking libcamera..."
ln -sf /usr/lib/python3/dist-packages/libcamera \
    ~/sign_project/lib/python3.11/site-packages/ 2>/dev/null

echo ""
echo "=================================="
echo "  Setup Complete!"
echo "  Run: python3 src/main.py"
echo "=================================="
