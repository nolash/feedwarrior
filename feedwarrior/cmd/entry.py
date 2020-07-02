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
    entry_path = os.path.join(config.entries_dir, uu)
    f = None
    if args.z:
        entry_path += '.gz'
        f = gzip.open(entry_path, 'xb')
    else:
        f = open(entry_path, 'x')
    feeds_entries_dir = os.path.join(config.feeds_dir, str(feed.uuid), 'entries')
    try:
        os.mkdir(feeds_entries_dir)
    except FileExistsError:
        pass
    entry_json = json.dumps(entry_serialized)
    f.write(entry_json.encode('utf-8'))
    f.close()

    feeds_entry_path = os.path.join(feeds_entries_dir, uu)
    if args.z:
        feeds_entry_path += '.gz'
    os.symlink(entry_path, feeds_entry_path)

    feed.add(entry)
