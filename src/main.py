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
from feedwarrior.cmd import create as cmd_create
from feedwarrior.cmd import entry as cmd_entry
from feedwarrior.cmd import show as cmd_show

logging.basicConfig(level=logging.ERROR)
logg = logging.getLogger()


argparser = argparse.ArgumentParser(description='create and manipulate feedwarrior feeds')
argparser.add_argument('-l', help='feed log to operate on')
argparser.add_argument('-c', type=str, help='configuration file')
argparser.add_argument('-v', action='store_true', help='be verbose')
sub = argparser.add_subparsers()
# TODO: add subparser to same level flags as main parser
sub.dest = 'command'
sub_entry = sub.add_parser('entry', help='add entry to feed')
cmd_entry.parse_args(sub_entry)
sub_show = sub.add_parser('show', help='view feed log')
cmd_show.parse_args(sub_show)
sub_create = sub.add_parser('create', help='create new feed')
cmd_create.parse_args(sub_create)


args = argparser.parse_args(sys.argv[1:])
if args.v:
    logging.getLogger().setLevel(logging.DEBUG)

logg.debug('loading config {}'.format(args.c))
config = feedwarrior.load_config(args.c)


def get_feed_by_name(s):
    index_path = os.path.join(config.feeds_dir, 'names', s)
    resolved_path = os.path.realpath(index_path)
    os.stat(resolved_path)
    logg.debug('feed path {} resolves to {}'.format(index_path, resolved_path))
    return os.path.basename(resolved_path)

feed_current = None
if args.l != None:
    try:
        uu = feedwarrior.common.parse_uuid(args.l)
        feed_current = feedwarrior.feed(uu)
    except ValueError:
        try:
            uu = get_feed_by_name(args.l)
            feed_current = feedwarrior.feed(uu)
        except FileNotFoundError as e:
            sys.stderr.write('cannot resolve feed {}\n'.format(args.l))
            sys.exit(1)


cmd_mod = None
if args.command == 'create':
    feed_current = feedwarrior.feed(parent=feed_current)
    cmd_mod = cmd_create
elif args.command == 'entry':
    cmd_mod = cmd_entry
elif args.command == 'show' or args.command == None:
    if feed_current == None:
        sys.stderr.write('plesae speficy a feed for showing\n')
        sys.exit(1)
    feed_current = feedwarrior.load_feed(os.path.join(config.feeds_dir, str(feed_current.uuid)))
    cmd_mod = cmd_show
else:
    sys.stderr.write('invalid command {}\n'.format(args.command))
    sys.exit(1)

try:
    os.makedirs(config.entries_dir, mode=0o777, exist_ok=False)
    os.makedirs(config.feeds_dir, mode=0o777, exist_ok=False)
    os.makedirs(os.path.join(config.feeds_dir, 'names'), mode=0o777, exist_ok=False)
    logg.debug('creating datadir {}'.format(config.data_dir))
except FileExistsError as e:
    logg.debug('using datadir {}'.format(config.data_dir))

if __name__ == '__main__':
    cmd_mod.execute(config, feed_current, args)
