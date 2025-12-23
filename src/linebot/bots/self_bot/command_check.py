from .command import Command
from .kicker_function import KickerFunction

class CommandCheck:
    def __init__(self):
        pass

    def is_command(self, text):
        if text:
            class_ = Command
            if text.startswith('k.'):
                class_ = KickerFunction
                text = text[2:]
            if ':' in text:
                mode = 'st'
            else:
                mode = 'is'
                command_name = text
            if mode == 'st':
                command_name = text.split(':')[0]
            coro_name = f"{mode}_{command_name}"
            if coro_name in dir(class_):
                coro = getattr(class_, coro_name)
                return coro

