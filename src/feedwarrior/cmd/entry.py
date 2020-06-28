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
    argparser.add_argument('--task', action='append', help='add taskwarrior task uuid relation')
    argparser.add_argument('path', help='multipart file to use for content')
    return True


def check_args(args):
    pass


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
    f = open(entry_path, 'x')
    feeds_entries_dir = os.path.join(config.feeds_dir, str(feed.uuid), 'entries')
    try:
        os.mkdir(feeds_entries_dir)
    except FileExistsError:
        pass
    json.dump(entry_serialized, f)
    f.close()

    feeds_entry_path = os.path.join(feeds_entries_dir, uu)
    os.symlink(entry_path, feeds_entry_path)
