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
        self.task_dir = os.path.join(os.environ.get('HOME'), '.task')
        cp = configparser.ConfigParser()

        config_paths = [filename]
        config_loaded = False
   
        # TODO: this make no sense
        # if filename == None:
        config_paths += BaseDirectory.load_config_paths('feedwarrior')

        if filename != None:
            for p in config_paths:
                config_path = os.path.join(p, filename)
                r = cp.read(config_path)
                if len(r) == 0:
                    logg.warning("config file in path {} not found".format(config_path))
                    continue

                logg.info('successfully read config {}'.format(p))
                config_loaded = True

        if cp.has_option('FEEDWARRIOR', 'datadir'):
            self.data_dir = cp['FEEDWARRIOR']['datadir']

        if cp.has_option('FEEDWARRIOR', 'taskdir'):
            self.task_dir = cp['FEEDWARRIOR']['taskdir']

        logg.info('using data dir {}'.format(self.data_dir))
        logg.info('using task dir {}'.format(self.task_dir))

        self.feeds_dir = os.path.join(self.data_dir, 'feeds')
        self.alias_dir = os.path.join(self.feeds_dir, 'names')
        self.entries_dir = os.path.join(self.data_dir, 'entries')
        self.hasher = hashlib.sha256


def load_config(filename):
    return config(filename)
