# standard imports
import email
import logging
import uuid
import json

# local imports
import feedwarrior

logg = logging.getLogger()


def parse_args(argparser):
    argparser.add_argument('-l', required=True, help='log to add entry to')
    argparser.add_argument('path', help='multipart file to use for content')
    return True


def check_args(args):
    pass


    return feedwarrior.entry(uu, m.get_payload())


def execute(config, feed, args):
    entry = feedwarrior.entry.from_multipart_file(args.path)
    entry_serialized = entry.serialize()
    uu = str(entry.uuid)
    logg.debug('adding entry {}'.format(uu))
    f = open(os.path.join(config.entries_dir, uu)
    json.dump(f, entry_serialized)
    f.close()
