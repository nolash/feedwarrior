# standard imports
import os
import gzip
import logging
import json

logg = logging.getLogger()


class fileadapter:

    def __init__(self, db_directory, uu):
        try:
            os.mkdir(os.path.join(db_directory, 'feeds'))
        except FileExistsError:
            pass

        try:
            os.mkdir(os.path.join(db_directory, 'feeds', str(uu)))
        except FileExistsError:
            pass

        try:
            os.mkdir(os.path.join(db_directory, 'entries'))
        except FileExistsError:
            pass

        try:
            os.mkdir(os.path.join(db_directory,  'feeds', str(uu), 'entries'))
        except FileExistsError:
            pass

        self.src = db_directory
        self.feeds_uuid = uu


    def get(self, uu, **kwargs):
        entry_path = os.path.join(self.src, 'entries', str(uu))
        f = None
        if entry_path[len(entry_path)-3:] == '.gz':
            logg.debug('uncompressing {}'.format(entry_path))
            f = gzip.open(entry_path, 'rb')
        else:
            f = open(entry_path, 'r')
        c = f.read()
        f.close()
        return c


    def put(self, uu, entry, **kwargs):

        entry_serialized = entry.serialize()
        entry_json = json.dumps(entry_serialized)
        contents_bytes = entry_json.encode('utf-8')

        entry_path = os.path.join(self.src, 'entries', str(uu))
        if os.path.exists(entry_path) or os.path.exists(entry_path + '.gz'):
            raise FileExistsError('record {} already exists'.format(str(uu)))
        f = None
        if kwargs.get('compress') != None:
            entry_path += '.gz'
            f = gzip.open(entry_path, 'xb')
        else:
            f = open(entry_path, 'xb')
            
        f.write(contents_bytes)
        f.close()

        feeds_entry_path = os.path.join(self.src, 'feeds', str(self.feeds_uuid), 'entries', str(uu))
        if kwargs.get('compress') != None:
            feeds_entry_path += '.gz'
        os.symlink(entry_path, feeds_entry_path)
