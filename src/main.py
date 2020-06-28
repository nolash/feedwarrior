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

cmd = 'log'
if args.command != None:
    log.error('invalid command {}'.format(args.command))
    sys.exit(1)

cmd_mod = None
if cmd == 'log':
    from feedwarrior.cmd import log as cmd_mod

try:
    os.mkdir(DATA_DIR)
    logg.debug('creating datadir {}'.format(DATA_DIR))
except FileExistsError as e:
    logg.debug('using datadir {}'.format(DATA_DIR))

if __name__ == '__main__':
