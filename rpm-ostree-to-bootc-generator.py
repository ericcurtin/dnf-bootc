#!/usr/bin/python3

import json
import rpm
import subprocess
import sys

def get_installed_pkgs():
    ts = rpm.TransactionSet()
    mi = ts.dbMatch()
    installed_pkgs = [hdr[rpm.RPMTAG_NAME] for hdr in mi]
    return installed_pkgs

def parse_rpm_ostree_status():
    # Run the rpm-ostree status --json command and capture the output
    result = subprocess.run(['rpm-ostree', 'status', '--json'], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to run rpm-ostree status --json: {result.stderr}")

    # Load the JSON data from the command output
    data = json.loads(result.stdout)

    booted_deployment = None

    # Find the booted deployment
    for deployment in data['deployments']:
        if deployment.get('booted'):
            booted_deployment = deployment
            break

    if not booted_deployment:
        raise ValueError("No booted deployment found")

    req_pkgs = booted_deployment.get('requested-packages', [])
    req_local_pkgs = booted_deployment.get('requested-local-packages', [])

    return req_pkgs, req_local_pkgs

def generate_containerfile(req_pkgs, req_local_pkgs, installed_pkgs):
    containerfile_content = f"FROM {base_image}\n"

    # Abbreviate package names
    pkgs = []
    for pkg in req_pkgs + req_local_pkgs:
        print(pkg)
        for installed_pkg in installed_pkgs:
            print(installed_pkg)
            print(pkg)
            if pkg.startswith(installed_pkg + "-") or pkg == installed_pkg:
                pkgs.append(installed_pkg)
                break

    containerfile_content += "RUN dnf install -y " + " ".join(pkgs) + "\n"

    # Write the Containerfile content to a file
    with open("/var/Containerfile", "w") as containerfile:
        containerfile.write(containerfile_content)

# Get the list of installed pkgs
installed_pkgs = get_installed_pkgs()

# Parse the JSON output from the rpm-ostree status --json command
req_pkgs, req_local_pkgs = parse_rpm_ostree_status()

if len(sys.argv) < 2:
    print("usage: rpm-ostree-to-bootc FROM")
    exit(0)

base_image = sys.argv[1]

# Generate Containerfile with the requested pkgs
generate_containerfile(req_pkgs, req_local_pkgs, installed_pkgs)

