# standard imports
import copy
import json
import uuid

# third party imports
import pycouchdb

class couchdbadapter:

    def __init__(self, username, password, database='feedwarrior', host='localhost', port=5984, ssl=False):
        scheme = 'http'
        if ssl:
            scheme += 's'
        dsn = '{}://{}:{}@{}:{}'.format(scheme, username, password, host, port)
        self.server = pycouchdb.Server(dsn)
        self.database = self.server.database(database)
        self.dsn = dsn
        self.username = username
        self.password = password
       

    def put(self, uu, entry, **kwargs):
        e = entry.serialize()
        e.pop('uuid')
        e['_id'] =uu.hex
        self.database.save(e)


    def get(self, uu, **kwargs):
        e = self.database.get(uu.hex)
        # reverse parsing this is going to take a bit of effort
        print('entry ZZZZZZZZZZZZZZZZZZZZZZZZz', e)
