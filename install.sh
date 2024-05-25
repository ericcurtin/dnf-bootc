#!/bin/bash

main() {
  set -eu -o pipefail

  local tmp="$(mktemp -d)"
  local url="raw.githubusercontent.com/ericcurtin/dnf-bootc/main"
  curl -fsSL -o "$tmp/dnf-bootc" "https://$url/dnf-bootc"
  curl -fsSL -o "$tmp/bootc.py" "https://$url/bootc.py"
  install -D -m755 "$tmp/dnf-bootc" "/var/dnf-bootc"
  install -D -m755 "$tmp/bootc.py" "/var/dnf-plugins/bootc.py"
  rm -rf $tmp &
}

main

