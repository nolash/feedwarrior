# standard imports
import uuid
import copy
import time
from .feedwarrior import parse_uuid


class feed:

    def __init__(self, uu=None, parent=None, created=None, updated=None):
        if uu == None:
            self.uuid = uuid.uuid4()
        else:
            self.uuid = parse_uuid(uu)

        self.parent = None
        if parent != None:
            if type(parent).__name__ != 'feed':
                raise ValueError('wrong type for parent: {}'.format(type(parent).__name__))
            self.parent = parent

        if created != None:
            self.created = created
            if updated == None:
                self.updated = copy.copy(created)
        else:
            self.created = int(time.time())
            self.updated = copy.copy(self.created)

        if self.updated == None:
            self.updated = updated

        self.entries = []


    def serialize(self):
        o = {
            'uuid': str(self.uuid),
            'created': self.created,
            'updated': self.updated,
                }
        if self.parent != None:
            o['parent_uuid'] = str(self.parent.uuid)
        
        return o
