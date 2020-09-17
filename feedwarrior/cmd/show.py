# standard imports
import json
import email
import time
import sys
import logging

logg = logging.getLogger(__file__)

def parse_args(argparser):
    pass

def check_args(args):
    pass

# TODO: this should call a render method of the entry instead of 
# dictating how the display format should be
def execute(config, feed, args):
    i = 0
    while 1:
        try:
            e = feed.next_entry()
        except IndexError as e:
            break
        j = json.loads(e)
        m = email.message_from_string(j['payload'])
        tf = email.utils.parsedate(m.get('Date'))
        t = int(time.mktime(tf))
        tl = time.localtime(t)
        ts = time.strftime('%x %X', tl)
        body = ''
        attachments = []
        ii = 0
        for p in m.walk():
            ii += 1
            if ii == 1:
                continue

            if 'attachment' in p.get_content_disposition():
                attachments.append('{} ({})'.format(p.get_filename(), p.get_content_type()))
            elif p.get_content_maintype() == 'text':
                subject = p.get('Subject')
                if subject == None:
                    subject = p.get_filename()
                #if p.get_filename() == '_content' or body == None:
                body += '>>> {}\n\n{}\n\n\n'.format(subject, p.get_payload(decode=True).decode('utf-8'))

        if i > 0:
           sys.stdout.write('----\n')

        if body != None:
            if args.headers:
                for k in m.keys():
                    print('{}: {}'.format(k, m.get(k)))
            sys.stdout.write('{} - {}\n'.format(ts, j['uuid']))
            sys.stdout.write('{}'.format(body))
            for a in attachments:
                sys.stdout.write('+ {}\n'.format(a))

        i += 1
    sys.stdout.flush()
