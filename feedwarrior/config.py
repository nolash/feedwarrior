# standard imports
import os
import configparser
import hashlib
import logging

# third party imports
from xdg import BaseDirectory

logg = logging.getLogger()


class config:

    def __init__(self, filename=None):
        self.data_dir = BaseDirectory.save_data_path('feedwarrior')
        cp = configparser.ConfigParser()

        config_paths = [filename]
        config_loaded = False
    
        if filename == None:
            config_paths = BaseDirectory.load_config_paths('feedwarrior')

        if filename != None:
            for p in config_paths:
                try:
                    cp.read(filename)
                    logg.info('successfully read config {}'.format(p))
                    config_loaded = True
                    break
                except FileNotFoundError:
                    logg.debug('config file {} not found'.format(p))
                    pass

        if cp.has_option('FEEDWARRIOR', 'datadir'):
            self.data_dir = cp['FEEDWARRIOR']['datadir']

        self.feeds_dir = os.path.join(self.data_dir, 'feeds')
        self.alias_dir = os.path.join(self.feeds_dir, 'names')
        self.entries_dir = os.path.join(self.data_dir, 'entries')
        self.hasher = hashlib.sha256


def load_config(filename):
    return config(filename)
