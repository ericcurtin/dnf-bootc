# DNF Bootc Plugin

The goal is to make an image-based OS, feel like a package-based OS.

UNTESTED, just a concept right now, the goal is so dnf-bootc behaves like dnf on a package based system to the end user.

This project provides a `dnf` plugin and a wrapper script `dnf-bootc` that automatically appends `dnf install` commands to a `Containerfile` and rebuilds the container using `podman build` after each successful installation.

## Features

- Automatically appends installed packages to `/var/Containerfile`.
- Rebuilds using `podman build` after each installation of a package.
- Only triggers when using `dnf-bootc` command, not when using `dnf` command.

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/ericcurtin/dnf-bootc/main/install.sh | sudo bash
```

## Usage

`dnf-bootc` uses the same syntax as `dnf`:

```bash
sudo dnf-bootc install <package_name>
```

