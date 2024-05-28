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
            new_containerfile_contents = self.update_containerfile(from_line, actions, "Containerfile")
            self.write_containerfile(new_containerfile_contents, "Containerfile", 'w')
            new_containerfile_contents = self.update_containerfile_unsquashed(from_line, actions, "Containerfile-unsquashed")
            self.write_containerfile(new_containerfile_contents, "Containerfile-unsquashed", 'a')

    def generate_actions(self):
        actions = []
        if self.pkgs_install:
            actions.append("COPY cache/dnf /var/cache/dnf")
            actions.append(f"RUN dnf install -y {' '.join(self.pkgs_install)} && dnf clean all")

        if self.pkgs_remove:
            actions.append(f"RUN dnf remove -y {' '.join(self.pkgs_remove)}")

        return actions

    def get_os_from_bootc_status(self):
        data = subprocess.run(["bootc", "status"], capture_output=True, text=True, check=True)
        data = yaml.safe_load(data.stdout)
        image = data['spec']['image']['image']
        return f"FROM {image}\n"

    def update_containerfile(self, from_line, actions, containerfile):
        new_containerfile_contents = from_line
        for action in actions:
            new_containerfile_contents += f"{action}\n"

        return new_containerfile_contents

    def update_containerfile_unsquashed(self, from_line, actions, containerfile):
        new_containerfile_contents = ""
        if not exists("/var/" + containerfile):
            new_containerfile_contents = from_line

        for action in actions:
            new_containerfile_contents += f"{action}\n"

        return new_containerfile_contents

    def write_containerfile(self, new_containerfile_contents, fname, mode):
        with open("/var/" + fname, mode) as f:
            f.write(new_containerfile_contents)

