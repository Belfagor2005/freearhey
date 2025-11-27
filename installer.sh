#!/bin/bash

version='3.1'
changelog='\nAdd Channel Change in to Player\n'

TMPPATH=/tmp/freearhey-install
FILEPATH=/tmp/freearhey-main.tar.gz

echo "Starting freearhey installation..."

if [ ! -d /usr/lib64 ]; then
    PLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions/freearhey
else
    PLUGINPATH=/usr/lib64/enigma2/python/Plugins/Extensions/freearhey
fi

cleanup() {
    echo "Cleaning up temporary files..."
    [ -d "$TMPPATH" ] && rm -rf "$TMPPATH"
    [ -f "$FILEPATH" ] && rm -f "$FILEPATH"
    [ -d "/tmp/freearhey-main" ] && rm -rf "/tmp/freearhey-main"
}

detect_os() {
    if [ -f /var/lib/dpkg/status ]; then
        OSTYPE="DreamOs"
        STATUS="/var/lib/dpkg/status"
    elif [ -f /etc/opkg/opkg.conf ] || [ -f /var/lib/opkg/status ]; then
        OSTYPE="OE"
        STATUS="/var/lib/opkg/status"
    else
        OSTYPE="Unknown"
        STATUS=""
    fi
    echo "Detected OS type: $OSTYPE"
}

detect_os

cleanup
mkdir -p "$TMPPATH"

if ! command -v wget >/dev/null 2>&1; then
    echo "Installing wget..."
    case "$OSTYPE" in
        "DreamOs")
            apt-get update && apt-get install -y wget || { echo "Failed to install wget"; exit 1; }
            ;;
        "OE")
            opkg update && opkg install wget || { echo "Failed to install wget"; exit 1; }
            ;;
        *)
            echo "Unsupported OS type. Cannot install wget."
            exit 1
            ;;
    esac
fi

if python --version 2>&1 | grep -q '^Python 3\.'; then
    echo "Python3 image detected"
    PYTHON="PY3"
    Packagerequests="python3-requests"
else
    echo "Python2 image detected"
    PYTHON="PY2"
    Packagerequests="python-requests"
fi

install_pkg() {
    local pkg=$1
    if [ -z "$STATUS" ] || ! grep -qs "Package: $pkg" "$STATUS" 2>/dev/null; then
        echo "Installing $pkg..."
        case "$OSTYPE" in
            "DreamOs")
                apt-get update && apt-get install -y "$pkg" || { echo "Could not install $pkg, continuing anyway..."; }
                ;;
            "OE")
                opkg update && opkg install "$pkg" || { echo "Could not install $pkg, continuing anyway..."; }
                ;;
            *)
                echo "Cannot install $pkg on unknown OS type, continuing..."
                ;;
        esac
    else
        echo "$pkg already installed"
    fi
}

install_pkg "$Packagerequests"

if [ "$OSTYPE" = "OE" ]; then
    echo "Installing additional multimedia packages..."
    for pkg in ffmpeg gstplayer exteplayer3 enigma2-plugin-systemplugins-serviceapp; do
        install_pkg "$pkg"
    done
fi

echo "Downloading freearhey..."
wget --no-check-certificate 'https://github.com/Belfagor2005/freearhey/archive/refs/heads/main.tar.gz' -O "$FILEPATH"
if [ $? -ne 0 ]; then
    echo "Failed to download freearhey package!"
    cleanup
    exit 1
fi

echo "Extracting package..."
tar -xzf "$FILEPATH" -C "$TMPPATH"
if [ $? -ne 0 ]; then
    echo "Failed to extract freearhey package!"
    cleanup
    exit 1
fi

echo "Installing plugin files..."
mkdir -p "$PLUGINPATH"

if [ -d "$TMPPATH/freearhey-main/usr/lib/enigma2/python/Plugins/Extensions/freearhey" ]; then
    cp -r "$TMPPATH/freearhey-main/usr/lib/enigma2/python/Plugins/Extensions/freearhey"/* "$PLUGINPATH/" 2>/dev/null
    echo "Copied from standard plugin directory"
elif [ -d "$TMPPATH/freearhey-main/usr/lib64/enigma2/python/Plugins/Extensions/freearhey" ]; then
    cp -r "$TMPPATH/freearhey-main/usr/lib64/enigma2/python/Plugins/Extensions/freearhey"/* "$PLUGINPATH/" 2>/dev/null
    echo "Copied from lib64 plugin directory"
elif [ -d "$TMPPATH/freearhey-main/usr" ]; then
    cp -r "$TMPPATH/freearhey-main/usr"/* /usr/ 2>/dev/null
    echo "Copied entire usr structure"
else
    echo "Could not find plugin files in extracted archive"
    echo "Available directories in tmp:"
    find "$TMPPATH" -type d | head -10
    cleanup
    exit 1
fi

sync

echo "Verifying installation..."
if [ -d "$PLUGINPATH" ] && [ -n "$(ls -A "$PLUGINPATH" 2>/dev/null)" ]; then
    echo "Plugin directory found and not empty: $PLUGINPATH"
    echo "Contents:"
    ls -la "$PLUGINPATH/" | head -10
else
    echo "Plugin installation failed or directory is empty!"
    cleanup
    exit 1
fi

cleanup
sync

FILE="/etc/image-version"
box_type=$(head -n 1 /etc/hostname 2>/dev/null || echo "Unknown")
distro_value=$(grep '^distro=' "$FILE" 2>/dev/null | awk -F '=' '{print $2}')
distro_version=$(grep '^version=' "$FILE" 2>/dev/null | awk -F '=' '{print $2}')
python_vers=$(python --version 2>&1)

cat <<EOF

#########################################################
#          freearhey $version INSTALLED SUCCESSFULLY     #
#                developed by LULULLA                   #
#               https://corvoboys.org                   #
#########################################################
#           your Device will RESTART Now                #
#########################################################
^^^^^^^^^^Debug information:
BOX MODEL: $box_type
OS SYSTEM: $OSTYPE
PYTHON: $python_vers
IMAGE NAME: ${distro_value:-Unknown}
IMAGE VERSION: ${distro_version:-Unknown}
EOF

echo "Restarting enigma2 in 3 seconds..."
sleep 3

if command -v systemctl >/dev/null 2>&1; then
    systemctl restart enigma2
elif command -v init >/dev/null 2>&1; then
    init 4 && sleep 2 && init 3
else
    killall -9 enigma2
fi

exit 0