#!/bin/bash
## setup command=wget -q --no-check-certificate https://raw.githubusercontent.com/Belfagor2005/freearhey/main/installer.sh -O - | /bin/sh

version='3.1'
changelog='\nAdd Channel Change in to Player\n'
TMPPATH=/tmp/freearhey-main
FILEPATH=/tmp/freearhey.tar.gz

if [ ! -d /usr/lib64 ]; then
    PLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions/freearhey
else
    PLUGINPATH=/usr/lib64/enigma2/python/Plugins/Extensions/freearhey
fi

if [ -f /var/lib/dpkg/status ]; then
    STATUS=/var/lib/dpkg/status
    OSTYPE=DreamOs
else
    STATUS=/var/lib/opkg/status
    OSTYPE=Dream
fi

if ! command -v wget >/dev/null; then
    if [ "$OSTYPE" = "DreamOs" ]; then
        apt-get update && apt-get install -y wget || { echo "Failed to install wget"; exit 1; }
    else
        opkg update && opkg install wget || { echo "Failed to install wget"; exit 1; }
    fi
fi

if python --version 2>&1 | grep -q '^Python 3\.'; then
    PYTHON=PY3
    Packagerequests=python3-requests
else
    PYTHON=PY2
    Packagerequests=python-requests
fi

if ! grep -qs "Package: $Packagerequests" "$STATUS"; then
    echo "Installing $Packagerequests..."
    if [ "$OSTYPE" = "DreamOs" ]; then
        apt-get update && apt-get install -y "$Packagerequests" || { echo "Failed to install $Packagerequests"; exit 1; }
    else
        opkg update && opkg install "$Packagerequests" || { echo "Failed to install $Packagerequests"; exit 1; }
    fi
fi

[ -d "$TMPPATH" ] && rm -rf "$TMPPATH"
[ -f "$FILEPATH" ] && rm -f "$FILEPATH"

mkdir -p "$TMPPATH" || { echo "Failed to create temp directory"; exit 1; }
cd "$TMPPATH" || exit 1

wget --no-check-certificate 'https://github.com/Belfagor2005/freearhey/archive/refs/heads/main.tar.gz' -O "$FILEPATH" || {
    echo "Download failed"; exit 1;
}

tar -xzf "$FILEPATH" -C /tmp/ || {
    echo "Extraction failed"; exit 1;
}

cp -r /tmp/freearhey-main/usr/ / || {
    echo "Copy failed"; exit 1;
}

if [ "$OSTYPE" != "DreamOs" ]; then
    opkg update && opkg install ffmpeg gstplayer exteplayer3 enigma2-plugin-systemplugins-serviceapp || {
        echo "Failed to install player dependencies"; exit 1;
    }
fi

if [ ! -d "$PLUGINPATH" ]; then
    echo "Installation failed: $PLUGINPATH missing"
    exit 1
fi

rm -rf "$TMPPATH" "$FILEPATH" /tmp/freearhey-main
sync

box_type=$(head -n 1 /etc/hostname 2>/dev/null || echo "Unknown")
distro_value=$(grep '^distro=' "/etc/image-version" 2>/dev/null | awk -F '=' '{print $2}')
distro_version=$(grep '^version=' "/etc/image-version" 2>/dev/null | awk -F '=' '{print $2}')
python_vers=$(python --version 2>&1)

echo "#########################################################
#          freearhey $version INSTALLED SUCCESSFULLY     #
#########################################################
BOX MODEL: $box_type
PYTHON: $python_vers
IMAGE: ${distro_value:-Unknown} ${distro_version:-Unknown}"

[ -f /usr/bin/enigma2 ] && killall -9 enigma2 || init 4 && sleep 2 && init 3
exit 0