import subprocess
from typing import Callable

import chardet


def run(cmd: str, on_info: Callable[[str], None] = None, on_error: Callable[[str], None] = None) -> int:
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.stderr:
        if on_error:
            on_error(_decode(result.stderr))
    else:
        if on_info:
            on_info(_decode(result.stdout))

    return result.returncode


def _decode(data: bytes) -> str:
    if data:
        encoding = chardet.detect(data)['encoding']
        return data.decode(encoding) if encoding else data.decode()

    return ''
