import os


def exist(iterable):
    return all(os.path.exists(path) for path in iterable)


def read_byte_by_byte(path):
    with open(path, 'rb') as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            yield byte
