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
        self.pkgs = []

    def resolved(self):
        for pkg in self.base.transaction.install_set:
            self.pkgs.append(pkg.name)

    def transaction(self):
        if self.pkgs:
            # This method is called after the transaction is executed
            containerfile_dir = '/var/Containerfile'
            containerfile_contents = ''
            if not exists(containerfile_dir):
                data = subprocess.run(["bootc", "status"], capture_output=True, text=True, check=True)
                data = data.stdout
                data = yaml.safe_load(data)

                # Extract the desired image value
                image = data['spec']['image']['image']
                containerfile_contents = f"FROM {image}\n"

            containerfile_contents = f"{containerfile_contents}RUN dnf install -y {' '.join(self.pkgs)}\n"
            with open(containerfile_dir, 'a') as f:
                f.write(containerfile_contents)

            print("Building bootc container")
            subprocess.run(['podman', 'build', '-t', 'os', '/var'], check=True)
            subprocess.run(['bootc', 'switch', '--transport', 'containers-storage', 'localhost/os'], check=True)

