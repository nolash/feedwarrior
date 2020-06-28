def parse_args(argparser):
    pass

def check_args(args):
    pass

def execute(config, feed, args):
    while 1:
        try:
            print(feed.next_entry())
        except IndexError:
            break
    pass
