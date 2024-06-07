# standard imports
import os
import email
import email.message
import email.utils
import uuid
import logging
import base64
import enum
import time
import gzip
import tempfile
import datetime

# local imports
from .common import defaulthashers
from .error import NotMultipartError

logg = logging.getLogger()

extensiontype = {
    'TASKWARRIOR': uuid.UUID
}

class extension(enum.Enum):
    TASKWARRIOR = 'TASKWARRIOR'
    pass

class entry:

    def __init__(self, uu, message):
        self.uuid = uu
        self.message = message
        self.extensions = {}


    def add_extension(self, k, v):
        if not isinstance(k, extension):
            raise ValueError('extension type {} invalid'.format(type(k)))
        requiredtyp = extensiontype[k.value]
        if not isinstance(v, requiredtyp):
            raise ValueError('extension value is {}, but {} is required'.format(type(v).__name__, requiredtyp))
        if self.extensions.get(k.value) == None:
           self.extensions[k.value] = []
        
        self.extensions[k.value].append(str(v))

        return True
            

    def serialize(self):

        for x in self.extensions.keys():
            logg.debug('adding extension header {}'.format(x))
            v = ','.join(self.extensions[x])
            self.message.add_header('X-FEEDWARRIOR-{}'.format(x), v)

        logg.debug('complete message {}'.format(self.message))

        d = email.utils.parsedate(self.message.get('Date'))
        logg.debug('date {} {}'.format(d, self.message.get('Date')))
        ts = time.mktime(d)

        return {
            'uuid': str(self.uuid),
            'timestamp': int(ts),
            'payload': self.message.as_string(),
                }


def to_multipart_file(path):
    #d = tempfile.TemporaryDirectory()
    #t = tempfile.NamedTemporaryFile(mode='w+', dir=d.name)

    basepath = os.path.basename(path)
    outpath = '.' + basepath + '_multipart'
    outpath = os.path.join(os.path.dirname(path), outpath)
    f = open(path, 'r')
    s = f.read()
    f.close()

    env = email.message.EmailMessage()
    env.add_header('Date', email.utils.formatdate())
    env.add_header('Content-Type', 'multipart/mixed')
    env.add_attachment(s)

    for msg in env.iter_attachments():
        msg.add_header('Subject', 'Entry added ' + email.utils.formatdate(localtime=True))
        msg.replace_header('Content-Disposition', 'inline')

    f = open(outpath, 'w')
    f.write(env.as_string())
    f.close()

    logg.debug("converted to multipath in " + outpath)

    return outpath

   

def from_multipart_file(filename, hashers=defaulthashers):
    f = None
    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        f = gzip.open(filename + '.gz', 'rb')
    m = email.message_from_file(f)
    f.close()
    return from_multipart(m, hashers)


def from_multipart(m, hashers=defaulthashers):
    if not m.is_multipart():
        raise NotMultipartError('not a MIME multipart message')

    # the hasher calculates a uuid from the canonical order of the message contents
    # TODO: currently the canonical order is the order of items in the message. this should
    # rather be the lexiographical order of the hash integer values of the items.
    htops = []
    hparts = {}
    for h in hashers:
        hasher = h()
        htops.append(h())
        hparts[hasher.name] = hasher

    # TODO: this is a naïve parser. If presumes that the message stucture will
    # always be a multipart container on top. Therefore it will always discard the top item
    subject = None
    i = 0
    for p in m.walk():
        if i == 0:
            subject = p.get('Subject')
            i += 1
            continue
        if p.get_content_maintype() == 'multipart':
            logg.warn('recursive multipart is not implemented, skipping part {}'.format(i))

        for htop in htops:
            hpart = hparts[htop.name]
            hpart.update(p.get_payload(decode=True))
            psum = hpart.digest()
            htop.update(psum)

        i += 1

    for h in htops:
        hasher = hparts[h.name]
        msum = hasher.digest()
        uu = uuid.UUID(bytes=msum[:16])
        #m.add_header('X-FEEDWARRIOR-HASH', htop.name)
        header_key = 'X-FEEDWARRIOR-{}'.format(h.name.upper())
        m.add_header(header_key, base64.encodebytes(msum).decode('ascii'))

    if subject == None:
        subject = str(uu)
        logg.info('subject not specified, using uuid {}'.format(subject))

    return entry(uu, m)

