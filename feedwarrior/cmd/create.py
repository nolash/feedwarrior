# standard imports
import os
import sys
import json
import logging

logg = logging.getLogger(__name__)

# TODO: move to submodule asap
def parse_args(argparser):
    argparser.add_argument('--alias', type=str, help='local common name for log')
    pass


def check_args(argparser):
    pass


def execute(config, feed, args):
    uu = str(feed.uuid)
    logg.debug('new feed {}'.format(uu))
    feed_path = os.path.join(config.feeds_dir, str(uu))
    os.mkdir(feed_path)
    os.mkdir(os.path.join(feed_path, 'entries'))
    if args.alias != None:
        alias_path = os.path.join(config.alias_dir, args.alias)
        os.symlink(feed_path, alias_path)

    feed_meta_path = os.path.join(feed_path, '.log')
    f = open(feed_meta_path, 'x')
    json.dump(feed.serialize(), f)
    f.close()
