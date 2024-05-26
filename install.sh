#!/bin/bash

main() {
  set -eu -o pipefail

  if [ "$EUID" -ne 0 ]; then
    echo "Error: This command has to be run with superuser privileges (under the root user on most systems)." >&2
    exit 1
  fi

  local tmp="$(mktemp -d)"
  local url="raw.githubusercontent.com/ericcurtin/dnf-bootc/s"
  curl -fsSL -o "$tmp/dnf-bootc" "https://$url/dnf-bootc"
  curl -fsSL -o "$tmp/bootc.py" "https://$url/bootc.py"
  install -D -m755 "$tmp/dnf-bootc" "/var/dnf-bootc"
  install -D -m755 "$tmp/bootc.py" "/var/dnf-plugins/bootc.py"
  echo "Complete!"
  rm -rf $tmp &
}

main

