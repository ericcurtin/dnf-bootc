# DNF Bootc Plugin

The goal is to make an image-based OS, feel like a package-based OS.

`/var/dnf-bootc` commands are applied live and persist after reboot.

## Features

- Automatically appends packages transactions to `/var/Containerfile`.
- Rebuilds using `podman build` after each modification of a package.
- Only triggers when using `/var/dnf-bootc` command, not when using `dnf` command.

## Features not available

Only installs and removes are available. Other features should be run and appended to `/var/Containerfile` manually. `/var/Containerfile` relies on keeping the state in sync with the local system, by appending a `RUN ` command to a previously known state in the `/var/Containerfile`.

An example of a feature that `/var/dnf-bootc` doesn't automatically account for would be, adding a third party repo. To do this, we may add lines to `/var/Containerfile` like this:

```bash
RUN dnf config-manager --add-repo repository
```

Followed by:

```bash
sudo cp /var/Containerfile /var/.Containerfile
```

This tells `/var/dnf-bootc`, we are happy to make manual changes to the `/var/Containerfile`, outside of it's management.

Followed by:

```bash
sudo dnf-bootc config-manager --add-repo repository
```

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/ericcurtin/dnf-bootc/main/install.sh | sudo bash
```

## Usage

Because we are not packaged properly yet, we have to call as `/var/dnf-bootc`.

`/var/dnf-bootc` uses the same syntax as `dnf`:

```bash
sudo /var/dnf-bootc install <package_name>
```

