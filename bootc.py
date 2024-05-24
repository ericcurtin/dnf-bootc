import subprocess
import dnf
import yaml
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
            containerfile_dir = '/var/Containerfile'
            containerfile_contents = ''
            if not exists(containerfile_dir):
                data = subprocess.run(["bootc", "status"], capture_output=True, text=True, check=True)
                data = yaml.safe_load(data.stdout)

                # Extract the desired image value
                image = data['spec']['image']['image']
                containerfile_contents = f"FROM {image}\n"

            containerfile_contents = f"{containerfile_contents}\n".join(actions) + '\n'
            with open(containerfile_dir, 'a') as f:
                f.write(containerfile_contents)

            print("Building bootc container")
            subprocess.run(['podman', 'build', '-t', 'os', '/var'], check=True)
            subprocess.run(['bootc', 'switch', '--transport', 'containers-storage', 'localhost/os'], check=True)

