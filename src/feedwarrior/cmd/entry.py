# standard imports
import os
import email
import logging
import uuid
import json

# local imports
import feedwarrior
from feedwarrior import entry as feedentry

logg = logging.getLogger()


def parse_args(argparser):
    argparser.add_argument('-l', required=True, help='log to add entry to')
    argparser.add_argument('--task', action='append', help='add taskwarrior task uuid relation')
    argparser.add_argument('path', help='multipart file to use for content')
    return True


def check_args(args):
    pass


def execute(config, feed, args):
    entry = feedentry.from_multipart_file(args.path)
    for t in args.task:
        uu = feedwarrior.common.parse_uuid(t)
        entry.add_extension(feedwarrior.extension.TASKWARRIOR, uu)

    entry_serialized = entry.serialize()
    uu = str(entry.uuid)
    logg.debug('adding entry {}'.format(uu))
    f = open(os.path.join(config.entries_dir, uu), 'x')
    json.dump(entry_serialized, f)
    f.close()
