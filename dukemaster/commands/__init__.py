from abc import abstractmethod

class BaseCommand(object):

    def __init__(self, data):
        """
        {'flags': {}, 'args': [], 'command': 'list', 'data': {'message_id': 'd1c8d2e5e93444e6b530145b982b7ea3', '__dukeclient__': {'version': '0.0.1-alpha'}}}
        """
        self.args = data['args']
        self.kwargs = data['flags']
        self.command = data['command']
        self._meta = data['data']

    @abstractmethod
    def call(self):
        pass
    

def call_command(data):
    cmd = data['command']
    class_name = '%sCommand' % (cmd[0].capitalize() + cmd[1:])
    module  = __import__('dukemaster.commands.%s' % cmd, {}, {}, class_name)
    command = getattr(module, class_name)(data)
    return command.call()
