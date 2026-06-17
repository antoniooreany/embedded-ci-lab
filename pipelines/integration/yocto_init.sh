#!/bin/bash
set -ex

# Define base paths
POKY_ROOT=${HOME}/yocto-work/poky
BUILD_DIR=$POKY_ROOT/build
BBLAYERS_CONF=$BUILD_DIR/conf/bblayers.conf
LOCAL_CONF=$BUILD_DIR/conf/local.conf
LAYER_PATH=${HOME}/yocto-work/yocto-lab/meta-yocto-lab

echo "Starting Yocto environment initialization..."
echo "Poky Root: $POKY_ROOT"
echo "Build Dir: $BUILD_DIR"

# 1. Initialize build directory if missing
# This script creates default local.conf and bblayers.conf
if [ ! -f "$BBLAYERS_CONF" ]; then
    echo "Initializing fresh build directory at $BUILD_DIR..."
    mkdir -p $BUILD_DIR
    source $POKY_ROOT/oe-init-build-env $BUILD_DIR
else
    echo "Build directory already exists, skipping initialization."
fi

# Double check configuration files presence
if [ ! -f "$BBLAYERS_CONF" ] || [ ! -f "$LOCAL_CONF" ]; then
    echo "Error: Configuration files were not created at $BUILD_DIR/conf/"
    exit 1
fi

# 2. Inject custom layer safely
# Idempotent check to avoid duplicate entries
if [ -d "$LAYER_PATH" ]; then
    echo "Injecting metadata layer: $LAYER_PATH"
    grep -q "$LAYER_PATH" "$BBLAYERS_CONF" || echo "BBLAYERS += \"$LAYER_PATH\"" >> "$BBLAYERS_CONF"
    echo "Layer status verified in $BBLAYERS_CONF"
else
    echo "Error: Metadata layer path not found at $LAYER_PATH"
    exit 1
fi

# 3. Automatically include custom application in the image
# Ensures the 'hello' package is installed in the final rootfs
echo "Configuring package installation in $LOCAL_CONF..."
if grep -q "IMAGE_INSTALL:append = \" hello\"" "$LOCAL_CONF"; then
    echo "Package 'hello' is already configured for installation."
else
    echo 'IMAGE_INSTALL:append = " hello"' >> "$LOCAL_CONF"
    echo "Successfully appended 'hello' to IMAGE_INSTALL in $LOCAL_CONF"
fi

echo "Yocto initialization complete."
