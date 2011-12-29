from dukemaster.commands import BaseCommand
from dukemaster.servers.models import Server
from dukemaster.projects.models import Project


class ListCommand(BaseCommand):
    """
    Returns a list of either projects or servers
    """

    def _list_servers(self):
        out = ["\n"]
        for server in Server.objects.all():
            out.append(" - %s: %s\n" % (server.name, server.hostname))
        return "".join(out)

    def _list_projects(self):
        out = ["\n"]
        for project in Project.objects.all():
            out.append(" - %s\n" % project.name)
        return "".join(out)

    def call(self):
        if self.args[0] == 'projects':
            self.out = self._list_projects()
        elif self.args[0] == 'servers':
            self.out = self._list_servers()
        else:
            self.out = "Error: unknown argument: %s" % self.args[0]

