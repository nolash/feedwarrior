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


    def get_raw_fp(self, fp):
        return open(fp, 'r')


    def get_gz_fp(self, fp):
        fp += '.gz'
        logg.debug('uncompressing {}'.format(fp))
        return gzip.open(fp, 'rb')
        #return open(fp, 'r')

    
    def get_with_type(self, uu, **kwargs):
        entry_path = os.path.join(self.src, 'entries', str(uu))
        f = None
        typ = 'plain'
        if entry_path[-3:] == '.gz':
            entry_path = entry_path[:-3]
        logg.debug('etnry {}'.format(entry_path))
        try:
            f = self.get_raw_fp(entry_path)
        except FileNotFoundError:
            f = self.get_gz_fp(entry_path)
            typ = 'gzip'
        c = f.read()
        f.close()
        return (c, typ,)


    def get(self, uu, **kwargs):
        r = self.get_with_type(uu, **kwargs)
        return r[0]

#        entry_path = os.path.join(self.src, 'entries', str(uu))
#        f = None
#        try:
#            f = self.get_raw_fp(entry_path)
#        except FileNotFoundError:
#            f = self.get_gz_fp(entry_path)
#        c = f.read()
#        f.close()
#        return c


    def put(self, uu, entry, replace=False, **kwargs):
        fm = 'xb'
        if replace:
            fm = 'wb'

        entry_serialized = entry.serialize()
        entry_json = json.dumps(entry_serialized)
        contents_bytes = entry_json.encode('utf-8')

        entry_path = os.path.join(self.src, 'entries', str(uu))
        if not replace and (os.path.exists(entry_path) or os.path.exists(entry_path + '.gz')):
            raise FileExistsError('record {} already exists'.format(str(uu)))
        f = None
        if kwargs.get('compress') != None:
            entry_path += '.gz'
            f = gzip.open(entry_path, fm)
        else:
            f = open(entry_path, fm)
            
        f.write(contents_bytes)
        f.close()

        feeds_entry_path = os.path.join(self.src, 'feeds', str(self.feeds_uuid), 'entries', str(uu))
        if kwargs.get('compress') != None:
            feeds_entry_path += '.gz'
        os.symlink(entry_path, feeds_entry_path)
