# standard imports
import email

def parse_args(argparser):
    argparser.add_argument('-l', required=True, help='log to add entry to')
    argparser.add_argument('path', help='multipart file to use for content')
    return True


def check_args(args):
    pass


def process_as_multipart_file(config, feed, filename):
    f = open(filename, 'r')
    m = email.message_from_file(f)
    f.close()
    if not m.is_multipart():
        raise ValueError('{} is not a MIME multipart message'.format(filename))
    pass

def execute(config, feed, args):
    process_as_mime(config, feed, args.path)
    pass
