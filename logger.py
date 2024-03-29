from typing import Callable


class Logger:
    _log = None

    @classmethod
    def init(cls, log: Callable[[str], None]):
        cls._log = log

    @classmethod
    def info(cls, message: str):
        if message:
            message = message.replace('I: ', '').replace('\r\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;')
            message = f'<font color="black">I: {message}</font>'
            cls._log(message)

    @classmethod
    def warn(cls, message: str):
        if message:
            message = message.replace('W: ', '').replace('\r\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;')
            message = f'<font color="orange">W: {message}</font>'
            cls._log(message)

    @staticmethod
    def error(message: str):
        if message:
            message = message.replace("E: ", "").replace('\r\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;')
            message = f'<font color="red">E: {message}</font>'
            Logger._log(message)
