#!/bin/bash
set -ex

POKY_ROOT=${HOME}/yocto-work/poky
BUILD_DIR=$POKY_ROOT/build
BBLAYERS_CONF=$BUILD_DIR/conf/bblayers.conf
LOCAL_CONF=$BUILD_DIR/conf/local.conf
LAYER_PATH=${HOME}/yocto-work/yocto-lab/meta-yocto-lab

# 1. Initialize build directory if missing
mkdir -p $BUILD_DIR/conf
if [ ! -f "$BBLAYERS_CONF" ]; then
    echo 'Initializing fresh build directory...'
    source $POKY_ROOT/oe-init-build-env $BUILD_DIR
fi

# 2. Inject custom layer safely
if [ -d "$LAYER_PATH" ]; then
    grep -q "$LAYER_PATH" "$BBLAYERS_CONF" || echo "BBLAYERS += \"$LAYER_PATH\"" >> "$BBLAYERS_CONF"
    echo 'Layers injected successfully'
else
    echo "Error: Layer path not found at $LAYER_PATH"
    exit 1
fi

# 3. Automatically include custom application in the image
# This ensures that the 'hello' package is installed in core-image-minimal
if [ -f "$LOCAL_CONF" ]; then
    grep -q "IMAGE_INSTALL:append = \" hello\"" "$LOCAL_CONF" || echo 'IMAGE_INSTALL:append = " hello"' >> "$LOCAL_CONF"
    echo 'Package hello added to IMAGE_INSTALL'
fi
