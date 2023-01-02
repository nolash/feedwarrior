# standard imports
import sys
import os
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
import email
import logging
import uuid
import json
import gzip
import tempfile
import base64
import uuid

# external imports
import magic
from mime_parser import parse_mime

# local imports
import feedwarrior
from feedwarrior import entry as feedentry
from feedwarrior.adapters import fileadapter
from feedwarrior.entry import from_multipart
#from feedwarrior.common import task_ids_to_uuids, check_task_uuids

logg = logging.getLogger()


def parse_args(argparser):
    argparser.add_argument('-e', '--entry', type=str, help='entry uuid to modify')
    argparser.add_argument('file', type=str, help='file to attach')
    return True


def check_args(args):
    pass


def from_file(m, fp):
    mg = magic.Magic(flags=magic.MAGIC_MIME_TYPE)
    mime_type_str = mg.id_filename(fp)
    mime_type = parse_mime(mime_type_str)
    logg.info('detected {} type for {}'.format(mime_type, fp))

    part = EmailMessage()
    part.add_header('Content-Type', mime_type_str)
    part.add_header('Content-Transfer-Encoding', 'BASE64')
    f = open(fp, 'rb')
    v = f.read()
    f.close()
    vb = base64.b64encode(v)
    part.set_payload(vb.decode('utf-8'))

    fn = os.path.basename(fp)
    part.add_header('Content-Disposition', 'attachment', filename=fn)

    m.attach(part)
    return m


def execute(config, feed, args):
    fa = fileadapter(config.data_dir, None)
    (v, fm) = fa.get_with_type(args.entry) #, compress=args.z)
    j = json.loads(v)
    m = email.message_from_string(j['payload'])

    fp = os.path.realpath(args.file)
    attachment = from_file(m, fp)
    
    entry = from_multipart(attachment)
    compress = fm == 'gzip'
    fa.put(args.entry, entry, replace=True, compress=compress)
