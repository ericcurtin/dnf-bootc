#!/bin/bash

install_755() {
  install -D -m755 "$1" "$2"
}

main() {
  set -eu -o pipefail

  if [ "$EUID" -ne 0 ]; then
    echo "Error: This command has to be run with superuser privileges (under the root user on most systems)." >&2
    exit 1
  fi

  local tmp="$(mktemp -d)"
  local url="https://raw.githubusercontent.com/ericcurtin/dnf-bootc/s"
  curl -fsSL -o "$tmp/dnf-bootc" "$url/dnf-bootc"
  curl -fsSL -o "$tmp/bootc-build-switch" "$url/bootc-build-switch"
  curl -fsSL -o "$tmp/rpm-ostree-to-bootc" "$url/rpm-ostree-to-bootc"
  curl -fsSL -o "$tmp/rpm-ostree-to-bootc.py" "$url/rpm-ostree-to-bootc.py"
  curl -fsSL -o "$tmp/bootc.py" "$url/bootc.py"
  install_755 "$tmp/dnf-bootc" "/var/dnf-bootc"
  install_755 "$tmp/bootc-build-switch" "/var/bootc-build-switch"
  install_755 "$tmp/rpm-ostree-to-bootc" "/var/rpm-ostree-to-bootc"
  install_755 "$tmp/rpm-ostree-to-bootc.py" "/var/rpm-ostree-to-bootc.py"
  install_755 "$tmp/bootc.py" "/var/dnf-plugins/bootc.py"
  echo "Complete!"
  rm -rf $tmp &
}

main

