# standard imports
import email
import os
import uuid
import copy
import time
import json
import logging
import gzip

# local imports
from feedwarrior.common import parse_uuid
from feedwarrior.adapters import fileadapter

logg = logging.getLogger()



class feed:

    def __init__(self, uu=None, parent=None, created=None, updated=None):
        if uu == None:
            self.uuid = uuid.uuid4()
        else:
            self.uuid = uu

        self.parent = None
        if parent != None:
            if type(parent).__name__ != 'feed':
                raise ValueError('wrong type for parent: {}'.format(type(parent).__name__))
            self.parent = copy.copy(parent)

        self.updated = 0
        self.created = 0
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
        self.entries_cursor = 0
        self.entries_sorted = False


    def add(self, entry):
        logg.debug('adding entry {}'.format(entry))
        self.entries.append(entry)


    def serialize(self):
        o = {
            'uuid': str(self.uuid),
            'created': self.created,
            'updated': self.updated,
                }
        if self.parent != None:
            o['parent_uuid'] = str(self.parent.uuid)
        
        return o


    # TODO: use index instead
    def _sort_entries(self):
        logg.debug('entries for {} {}'.format(self.uuid, self.entries))
        new_entries = []
        for e in self.entries:
            entry = self.getter.get(e)
            o = json.loads(entry)
            m = email.message_from_string(o['payload'])
            d = email.utils.parsedate(m.get('Date'))
            t = time.mktime(d)
            ts = str(t)
            if not m.is_multipart():
                raise ValueError('invalid entry {}'.format(e))
            logg.debug('date {} {}'.format(e, ts))
            new_entries.append('_'.join([ts, e]))

        self.entries = []
        new_entries.sort()
        for ne in new_entries:
            e = ne.split('_', maxsplit=1)
            self.entries.append(e[1])

        self.entries_cursor = 0
        self.entries_sorted = True


    def set_getter(self, getter):
        self.getter = getter


    def next_entry(self):
        if not self.entries_sorted:
            self._sort_entries()
        if self.entries_cursor == len(self.entries):
            raise IndexError('no more entries')

        e = self.getter.get(self.entries[self.entries_cursor])
        self.entries_cursor += 1
        return e



# TODO: add input checking for timestamps
# TODO: check state of symlink index
def load(data_dir, uu):
    path = os.path.join(data_dir, 'feeds', str(uu))
    feed_meta_path = os.path.join(path, '.log')
    f = open(feed_meta_path, 'r')
    o = json.load(f)
    uu = parse_uuid(o['uuid'])
    puu = None
    p = None
    if o.get('parent_uuid') != None:
        puu = parse_uuid(o['parent_uuid'])
        p = feed(puu) 
    feed_loaded = feed(uu, p, int(o['created']), int(o['updated']))

    feed_entries_path = os.path.join(path, 'entries')
    for entry in os.listdir(feed_entries_path):
        feed_loaded.entries.append(entry)

    fg = fileadapter(data_dir, uu)
    feed_loaded.set_getter(fg)

    return feed_loaded


