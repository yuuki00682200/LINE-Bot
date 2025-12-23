from .command import Command

class CommandCheck:
    def __init__(self, prefix):
        self.__commands = self.load_command_function()
        self.prefix = prefix

    def get_command(self, command):
        for prefix in self.prefix:
            if command.startswith(prefix):
                command = command.replace(prefix, "")
                if ":" in command:
                    command = command.split(":")[0] + ":"
                if command in self.__commands:
                    print(command)
                    return self.__commands[command], prefix
        return False, None
                
    def load_command_function(self):
        coroutines = filter(lambda x:x[:2] != "__", dir(Command))
        attrs = [getattr(Command, name) for name in coroutines]
        result = {}
        for coro in attrs:
            if coro.__doc__:
                doc = coro.__doc__
                if ";" in doc:
                    names = self.parse(doc)
                    for name in names:
                        result[name] = coro
        return result

    def parse(self, string):
        splited = string.split(";")[1]
        commands = splited.split(",")
        result = list(map(self.read_name, commands))
        return result
    
    def read_name(self, string):
        return string.strip()

