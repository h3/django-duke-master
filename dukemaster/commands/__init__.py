from abc import abstractmethod

from dukemaster.utils import simplejson
from dukemaster.utils.json import BetterJSONEncoder

class BaseCommand(object):
    output_format = 'raw'
    out = ''

    def __init__(self, data):
        """
        {'flags': {}, 'args': [], 'command': 'list', 'data': {'message_id': '', '__dukeclient__': {'version': ''}}}
        """
        self.args = data['args']
        self.kwargs = data['flags']
        self.command = data['command']
        self._meta = data['data']

    @abstractmethod
    def call(self):
        pass

    def output(self):
        if self.output_format == 'json':
            return simplejson.dumps(self.out, cls=BetterJSONEncoder)
        else:
            return self.out
    

def call_command(data):
    cmd = data['command']
    class_name = '%sCommand' % (cmd[0].capitalize() + cmd[1:])
    module  = __import__('dukemaster.commands.%s' % cmd, {}, {}, class_name)
    command = getattr(module, class_name)(data)
    command.call()
    return command.output()
