# standard imports
import os
import configparser
import hashlib

# third party imports
from xdg import BaseDirectory


class config:

    def __init__(self, filename=None):
        self.data_dir = BaseDirectory.save_data_path('feedwarrior')
        cp = configparser.ConfigParser()

        config_paths = [filename]
        config_loaded = False
        if filename == None:
            config_paths = BaseDirectory.load_config_paths('feedwarrior')

            for p in config_paths:
                try:
                    cp.read(filename)
                    break
                except FileNotFoundError:
                    pass

        if cp.has_section('FEEDWARRIOR'):
            self.data_dir = cp['FEEDWARRIOR'].get(['datadir'])

        self.feeds_dir = os.path.join(self.data_dir, 'feeds')
        self.entries_dir = os.path.join(self.data_dir, 'entries')
        self.hasher = hashlib.sha256


def load_config(filename):
    return config(filename)
