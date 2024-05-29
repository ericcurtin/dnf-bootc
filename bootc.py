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
        from_line = self.get_os_from_bootc_status()
        actions = self.generate_actions()
        if actions:
            new_contfile = self.update_containerfile(from_line, actions, "Containerfile")
            self.write_containerfile(new_contfile, "Containerfile", 'w')

        actions = self.generate_actions(unsquashed=True)
        if actions:
            new_contfile_unsq = self.update_containerfile(from_line, actions, "Containerfile-unsquashed", unsquashed=True)
            self.write_containerfile(new_contfile_unsq, "Containerfile-unsquashed", 'a')

    def generate_actions(self, unsquashed=False):
        actions = []
        if self.pkgs_install:
            if not unsquashed:
                actions.append("COPY cache/dnf /var/cache/dnf")

            actions.append(f"RUN dnf install -y {' '.join(self.pkgs_install)}" +
                           (" && dnf clean all" if not unsquashed else ""))

        if self.pkgs_remove:
            actions.append(f"RUN dnf remove -y {' '.join(self.pkgs_remove)}")

        return actions

    def get_os_from_bootc_status(self):
        data = subprocess.run(["bootc", "status"], capture_output=True, text=True, check=True)
        data = yaml.safe_load(data.stdout)
        image = data['spec']['image']['image']
        return f"FROM {image}\n"

    def update_containerfile(self, from_line, actions, containerfile, unsquashed=False):
        new_contfile = from_line if not unsquashed or not exists("/var/" + containerfile) else ""
        for action in actions:
            new_contfile += f"{action}\n"

        return new_contfile

    def write_containerfile(self, new_contfile, fname, mode):
        with open("/var/" + fname, mode) as f:
            f.write(new_contfile)

