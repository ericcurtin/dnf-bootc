#!/bin/bash

main() {
  set -eux

  local tmp="$(mktemp -d)"
  URL="raw.githubusercontent.com/ericcurtin/dnf-bootc/main"
  curl -fsSL -o "$tmp/dnf-bootc" "https://$URL/dnf-bootc"
  curl -fsSL -o "$tmp/bootc.py" "https://$URL/bootc.py"
  install -D -m755 "$tmp/dnf-bootc" "/var/dnf-bootc"
  install -D -m755 "$tmp/bootc.py" "/var/dnf-plugins/bootc.py"
  rm -rf $tmp &
}

main

