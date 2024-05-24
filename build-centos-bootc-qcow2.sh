#!/bin/bash

set -eu -o pipefail

# IMAGE="quay.io/fedora/fedora-bootc:40"
IMAGE="quay.io/centos-bootc/centos-bootc:stream9"

mkdir -p output
# Ensure the image is fetched
sudo podman pull $IMAGE
sudo podman run \
    --rm \
    -it \
    --privileged \
    --pull=newer \
    --security-opt label=type:unconfined_t \
    -v $(pwd)/config.toml:/config.toml \
    -v $(pwd)/output:/output \
    -v /var/lib/containers/storage:/var/lib/containers/storage \
    quay.io/centos-bootc/bootc-image-builder:latest \
    --type qcow2 \
    --local \
    $IMAGE

