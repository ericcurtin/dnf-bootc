# DNF Bootc Plugin

The goal is to make an image-based OS, feel like a package-based OS.

`/var/dnf-bootc` commands are applied live and persist after reboot.

## Features

- Automatically appends packages to `/var/Containerfile`.
- Rebuilds using `podman build` after each modification of a package.
- Only triggers when using `/var/dnf-bootc` command, not when using `dnf` command.

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/ericcurtin/dnf-bootc/main/install.sh | sudo bash
```

## Usage

Because we are not packaged properly yet, we have to call as `/var/dnf-bootc`

`/var/dnf-bootc` uses the same syntax as `dnf`:

```bash
sudo /var/dnf-bootc install <package_name>
```

