# standard imports
import os
import email
import logging
import uuid
import json
import gzip

# local imports
import feedwarrior
from feedwarrior import entry as feedentry
from feedwarrior.adapters import fileadapter

logg = logging.getLogger()


def parse_args(argparser):
    argparser.add_argument('-z', action='store_true', help='compress entry with gzip')
    argparser.add_argument('--task', action='append', help='add taskwarrior task uuid relation')
    argparser.add_argument('path', help='multipart file to use for content')
    return True


def check_args(args):
    pass


# TODO: move logic to package to get symmetry with the show.py logic
def execute(config, feed, args):
    entry = feedentry.from_multipart_file(args.path)
    if args.task != None:
        for t in args.task:
            uu = feedwarrior.common.parse_uuid(t)
            entry.add_extension(feedwarrior.extension.TASKWARRIOR, uu)

    entry_serialized = entry.serialize()
    uu = str(entry.uuid)
    logg.debug('adding entry {}'.format(uu))
    
    fa = fileadapter(config.data_dir, feed.uuid)

    entry_json = json.dumps(entry_serialized)
    fa.put(entry.uuid, entry_json.encode('utf-8'), args.z)
   
    feed.add(entry)
