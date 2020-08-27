# standard imports
import os

def parse_args(argparser):
    pass


def check_args(args):
    pass


def execute(config, feed, args):
    feeds_names_dir = os.path.join(config.feeds_dir, 'names')
    for f in os.listdir(feeds_names_dir):
        n = os.path.join(feeds_names_dir, f)
        r = os.path.realpath(n)
        print('{} {}'.format(os.path.basename(r), f))
