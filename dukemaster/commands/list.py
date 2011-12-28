from dukemaster.commands import BaseCommand
from dukemaster.servers.models import Server

class ListCommand(BaseCommand):

    def call(self, data):
        out = ["\n"]
        for server in Server.objects.all():
            out.append(" - %s: %s\n" % (server.name, server.hostname))
        return "".join(out)

