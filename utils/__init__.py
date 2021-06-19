import os


def check_file(fileName: str):
    """check file in path"""
    return os.path.isfile('{}'.format(fileName))

