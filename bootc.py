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
        actions = self.generate_actions()
        if actions:
            from_line = self.get_os_from_bootc_status()
            new_containerfile_contents = self.update_containerfile(from_line, actions)
            self.write_containerfile(new_containerfile_contents)

    def generate_actions(self):
        actions = []
        if self.pkgs_install:
            actions.append(f"RUN dnf install -y {' '.join(self.pkgs_install)}")

        if self.pkgs_remove:
            actions.append(f"RUN dnf remove -y {' '.join(self.pkgs_remove)}")

        return actions

    def get_os_from_bootc_status(self):
        data = subprocess.run(["bootc", "status"], capture_output=True, text=True, check=True)
        data = yaml.safe_load(data.stdout)
        image = data['spec']['image']['image']
        return f"FROM {image}\n"

    def update_containerfile(self, from_line, actions):
        containerfile = '/var/Containerfile'
        new_containerfile_contents = ''
        if exists(containerfile):
            with open(containerfile, 'r') as f:
                lines = f.readlines()

            replaced = False
            for line in lines:
                if line.startswith("FROM "):
                    new_containerfile_contents += from_line
                    replaced = True
                else:
                    new_containerfile_contents += line

            if not replaced:
                new_containerfile_contents = from_line + new_containerfile_contents
        else:
            new_containerfile_contents = from_line

        for action in actions:
            new_containerfile_contents += f"{action}\n"

        return new_containerfile_contents

    def write_containerfile(self, new_containerfile_contents):
        with open('/var/Containerfile', 'w') as f:
            f.write(new_containerfile_contents)

