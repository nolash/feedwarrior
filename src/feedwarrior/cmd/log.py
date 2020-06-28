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
    if args.command == None:
        uu = str(feed.uuid)
        logg.debug('new log {}'.format(uu))
        log_path = os.path.join(config.feeds_dir, str(uu))
        os.mkdir(log_path)

        log_meta_path = os.path.join(log_path, '.log')
        f = open(log_meta_path, 'x')
        json.dump(feed.serialize(), f)
    f.close()
