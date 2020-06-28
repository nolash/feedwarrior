# standard imports
import email
import uuid
import logging
import base64

# local imports
from .common import defaulthasher

logg = logging.getLogger()


class entry:

    def __init__(self, uu, payload):
        self.uuid = uu
        self.payload = payload


    def serialize(self):
        return {
            'uuid': str(self.uuid),
            'payload': self.payload,
                }

   

def from_multipart_file(filename, hasher=defaulthasher):
#def process_as_multipart_file(config, feed, filename):
    f = open(filename, 'r')
    m = email.message_from_file(f)
    f.close()
    if not m.is_multipart():
        raise ValueError('{} is not a MIME multipart message'.format(filename))

    # the hasher calculates a uuid from the canonical order of the message contents
    # TODO: currently the canonical order is the order of items in the message. this should
    # rather be the lexiographical order of the hash integer values of the items.
    htop = hasher()

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

        hpart = hasher()
        hpart.update(p.get_payload(decode=True))
        psum = hpart.digest()
        htop.update(psum)

        i += 1

    msum = htop.digest()
    uu = uuid.UUID(bytes=msum[:16])
    m.add_header('X-FEEDWARRIOR-HASH', htop.name)
    m.add_header('X-FEEDWARRIOR-DIGEST', base64.encodebytes(msum).decode('ascii'))

    if subject == None:
        subject = str(uu)
        logg.info('subject not specified, using uuid {}'.format(subject))

    return entry(uu, m.as_bytes())

