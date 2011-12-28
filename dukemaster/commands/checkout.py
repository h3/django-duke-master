from dukemaster.commands import BaseCommand
from dukemaster.projects.models import Project


class CheckoutCommand(BaseCommand):
    """
    Returns a list of either projects or servers
    """

    output_format = 'json'

    def call(self):
        project_name = self.args[0]
        try:
            project = Project.objects.get(name=project_name)
            print project.url
            self.out = {'protocol': project.protocol, 'url': project.url}
            return True
        except:
            return False

        #return "Error: unknown argument: %s" % self.args[0]


