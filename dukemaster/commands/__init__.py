from abc import abstractmethod

class BaseCommand(object):
    @abstractmethod
    def call(self):
        print "CALLING COMMAND"
    

def call_command(data):
    cmd = data['command']
    class_name = '%sCommand' % (cmd[0].capitalize() + cmd[1:])
    module  = __import__('dukemaster.commands.%s' % cmd, {}, {}, class_name)
    command = getattr(module, class_name)()
    return command.call(data)
