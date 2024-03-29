import os


def save(filename: str, content: str):
    with open(os.path.join(os.getcwd(), 'resources', filename), 'w', encoding='utf-8') as file:
        file.write(content)


def read(filename: str) -> str:
    path = os.path.join(os.getcwd(), 'resources', filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return ''
