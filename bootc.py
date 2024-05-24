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
            containerfile = '/var/Containerfile'
            containerfile_contents = ''
            if not exists(containerfile):
                data = subprocess.run(["bootc", "status"], capture_output=True, text=True, check=True)
                data = yaml.safe_load(data.stdout)

                # Extract the desired image value
                image = data['spec']['image']['image']
                containerfile_contents = f"FROM {image}\n"

            for action in actions:
                containerfile_contents += f"{action}\n"

            with open(containerfile, 'a') as f:
                f.write(containerfile_contents)

            # Calculate and write the SHA256 checksum
            sha256sum = hashlib.sha256()
            with open(containerfile, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256sum.update(chunk)

            with open('/var/Containerfile.sha256sum', 'w') as f:
                f.write(sha256sum.hexdigest())

            print("Building bootc container")
            subprocess.run(['podman', 'build', '-t', 'os', '/var'], check=True)
            subprocess.run(['bootc', 'switch', '--transport', 'containers-storage', 'localhost/os'], check=True)

