# standard imports
import os
import sys
import json
import logging

logg = logging.getLogger(__name__)

# TODO: move to submodule asap
def parse_args(argparser):
    pass


def check_args(argparser):
    pass


def execute(config, feed, args):
    uu = str(feed.uuid)
    logg.debug('new feed {}'.format(uu))
    feed_path = os.path.join(config.feeds_dir, str(uu))
    os.mkdir(feed_path)
    os.mkdir(os.path.join(feed_path, 'entries'))

    feed_meta_path = os.path.join(feed_path, '.log')
    f = open(feed_meta_path, 'x')
    json.dump(feed.serialize(), f)
    f.close()
