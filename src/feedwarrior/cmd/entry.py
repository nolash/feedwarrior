# standard imports
import email

def parse_args(argparser):
    argparser.add_argument('-l', required=True, help='log to add entry to')
    argparser.add_argument('path', help='multipart file to use for content')
    return True


def check_args(args):
    pass


def process_as_email(config, feed, payload):
    pass

def execute(config, feed, args):
    process_as_email(config, feed, args.path)
    pass
