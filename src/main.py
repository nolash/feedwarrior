#!/usr/bin/python

# Author: Louis Holbrook <dev@holbrook.no> (https://holbrook.no)
# License: GPLv3
# Description: Work log tool

# standard imports
import os
import sys
import argparse
import configparser
import json
import logging

# local imports
import feedwarrior

logging.basicConfig(level=logging.ERROR)
logg = logging.getLogger()

DATA_DIR='/dev/null'


argparser = argparse.ArgumentParser(description='create and manipulate feedwarrior logs')
argparser.add_argument('-p', type=str, help='parent log uuid')
argparser.add_argument('-c', required=True, type=str, help='configuration file')
argparser.add_argument('-v', action='store_true', help='be verbose')
sub = argparser.add_subparsers()
sub.dest = 'command'

args = argparser.parse_args(sys.argv[1:])
if args.v:
    logging.getLogger().setLevel(logging.DEBUG)

logg.debug('loading config {}'.format(args.c))
cp = configparser.ConfigParser()
cp.read(args.c)
DATA_DIR = cp['FEEDWARRIOR']['datadir']

try:
    os.mkdir(DATA_DIR)
    logg.debug('creating datadir {}'.format(DATA_DIR))
except FileExistsError as e:
    logg.debug('using datadir {}'.format(DATA_DIR))


# TODO: move to submodule asap
feed_parent = None
if args.p != None:
    try:
        feed_parent = feedwarrior.feed(args.p)
    except ValueError as e:
        logg.error('invalid parent {}: {}'.format(args.p, e))
        sys.exit(1)

if __name__ == '__main__':
    if args.command == None:
        feed_current = feedwarrior.feed(parent=feed_parent)
        uu = str(feed_current.uuid)
        logg.debug('new log {}'.format(uu))
        log_path = os.path.join(DATA_DIR, str(uu))
        os.mkdir(log_path)

        log_meta_path = os.path.join(log_path, '.log')
        f = open(log_meta_path, 'x')
        json.dump(feed_current.serialize(), f)
    f.close()
    sys.exit(0)
