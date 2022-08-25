#!/bin/bash

#set -o xtrace

echo "Update package definition and install additional packages based on PLATFORM"

. /ci-scripts/include.sh
ARCH="$(dpkg-architecture -q DEB_BUILD_ARCH)"
/ci-scripts/fix-product-repository.sh "${DEBIAN_VERSION}" "${PRODUCT}" "${ARCH}"

apt update
apt upgrade -y
apt update && apt install -y python3-jinja2 python3-yaml
apt install -y unipi-kernel-headers
