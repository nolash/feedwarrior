# standard imports
import configparser

class config:

    def __init__(self, filename):
        cp = configparser.ConfigParser()
        cp.read(filename)
        self.data_dir = cp['FEEDWARRIOR']['datadir']

def load_config(filename):
    return config(filename)
