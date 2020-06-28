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
from feedwarrior.cmd import log as cmd_log
from feedwarrior.cmd import entry as cmd_entry

logging.basicConfig(level=logging.ERROR)
logg = logging.getLogger()



argparser = argparse.ArgumentParser(description='create and manipulate feedwarrior logs')
argparser.add_argument('-p', type=str, help='parent log uuid')
argparser.add_argument('-c', required=True, type=str, help='configuration file')
argparser.add_argument('-v', action='store_true', help='be verbose')
sub = argparser.add_subparsers()
# TODO: add subparser to same level flags as main parser
sub.dest = 'command'
sub_entry = sub.add_parser('entry', help='add entry to log')
cmd_entry.parse_args(sub_entry)

args = argparser.parse_args(sys.argv[1:])
if args.v:
    logging.getLogger().setLevel(logging.DEBUG)

logg.debug('loading config {}'.format(args.c))
config = feedwarrior.load_config(args.c)


feed_current = None
feed_parent = None
if args.p != None:
    try:
        feed_parent = feedwarrior.feed(args.p)
    except ValueError as e:
        logg.error('invalid parent {}: {}'.format(args.p, e))
        sys.exit(1)

cmd_mod = None
if args.command == None:
    feed_current = feedwarrior.feed(parent=feed_parent)
    cmd_mod = cmd_log
elif args.command == 'entry':
    cmd_mod = cmd_entry
else:
    log.error('invalid command {}'.format(args.command))
    sys.exit(1)

try:
    os.mkdir(config.data_dir)
    logg.debug('creating datadir {}'.format(config.data_dir))
except FileExistsError as e:
    logg.debug('using datadir {}'.format(config.data_dir))

if __name__ == '__main__':
    cmd_mod.execute(config, feed_current, args)
