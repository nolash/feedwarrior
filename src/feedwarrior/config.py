# standard imports
import os
import configparser

class config:

    def __init__(self, filename):
        cp = configparser.ConfigParser()
        cp.read(filename)
        self.data_dir = cp['FEEDWARRIOR']['datadir']
        self.feeds_dir = os.path.join(cp['FEEDWARRIOR']['datadir'], 'feeds')
        self.entries_dir = os.path.join(cp['FEEDWARRIOR']['datadir'], 'entries')

def load_config(filename):
    return config(filename)
