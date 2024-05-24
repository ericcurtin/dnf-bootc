import subprocess
import dnf
import yaml
import shutil
from dnf.plugin import Plugin
from os.path import exists

class BootcPlugin(Plugin):
    name = 'bootc'

    def __init__(self, base, cli):
        super(BootcPlugin, self).__init__(base, cli)
        self.base = base
        self.cli = cli
        self.pkgs_install = []
        self.pkgs_remove = []

    def resolved(self):
        self.pkgs_install = [pkg.name for pkg in self.base.transaction.install_set]
        self.pkgs_remove = [pkg.name for pkg in self.base.transaction.remove_set]

    def transaction(self):
        actions = []
        if self.pkgs_install:
            actions.append(f"RUN dnf install -y {' '.join(self.pkgs_install)}")
        if self.pkgs_remove:
            actions.append(f"RUN dnf remove -y {' '.join(self.pkgs_remove)}")

        if actions:
            containerfile = '/var/Containerfile'
            new_containerfile_contents = ''
            from_line = ''

            data = subprocess.run(["bootc", "status"], capture_output=True, text=True, check=True)
            data = yaml.safe_load(data.stdout)

            # Extract the desired image value
            image = data['spec']['image']['image']
            from_line = f"FROM {image}\n"

            if exists(containerfile):
                with open(containerfile, 'r') as f:
                    lines = f.readlines()

                # Replace the FROM line if it exists
                replaced = False
                for line in lines:
                    if line.startswith("FROM "):
                        new_containerfile_contents += from_line
                        replaced = True
                    else:
                        new_containerfile_contents += line

                # If there was no FROM line, add it at the top
                if not replaced:
                    new_containerfile_contents = from_line + new_containerfile_contents
            else:
                new_containerfile_contents = from_line

            for action in actions:
                new_containerfile_contents += f"{action}\n"

            with open(containerfile, 'w') as f:
                f.write(new_containerfile_contents)

            shutil.copy("/var/Containerfile", "/var/.Containerfile")

            print("Building bootc container")
            subprocess.run(['podman', 'build', '-t', 'os', '/var'], check=True)
            subprocess.run(['bootc', 'switch', '--transport', 'containers-storage', 'localhost/os:latest'], check=True)

