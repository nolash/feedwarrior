# standard imports
import json
import email
import time

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
        except IndexError:
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
           print('----')

        if body != None:
            if args.headers:
                for k in m.keys():
                    print('{}: {}'.format(k, m.get(k)))
            print('{} - {}\n'.format(ts, j['uuid']))
            print(body)
            for a in attachments:
                print('+ {}'.format(a))

        i += 1
    pass
