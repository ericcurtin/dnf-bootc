#!/bin/bash

set -eux

ssh -p2222 user@127.0.0.1 "mkdir -p ~/var/dnf-plugins/"
scp -P2222 bootc-build-switch user@127.0.0.1:~/var/
scp -P2222 bootc.py user@127.0.0.1:~/var/dnf-plugins/
scp -P2222 dnf-bootc user@127.0.0.1:~/var/
ssh -p2222 user@127.0.0.1 "sudo cp -r ~/var/* /var/"

