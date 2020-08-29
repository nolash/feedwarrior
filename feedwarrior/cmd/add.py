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

# local imports
import feedwarrior
from feedwarrior import entry as feedentry
from feedwarrior.adapters import fileadapter
from feedwarrior.entry import extension
from feedwarrior.common import task_ids_to_uuids, check_task_uuids

logg = logging.getLogger()


def get_editor():
    return 'vim'

def parse_args(argparser):
    argparser.add_argument('-z', action='store_true', help='compress entry with gzip')
    argparser.add_argument('--task-id', dest='task_id', type=int, action='append', help='add taskwarrior task id relations translated to uuis (cannot be used with --task-uuid')
    argparser.add_argument('--task-uuid', dest='task_uuid', type=str, action='append', help='add taskwarrior task uuid relations (cannot be used with --task-id')
    argparser.add_argument('-s', type=str, help='entry subject')
    return True


def check_args(args):
    pass


# TODO: move logic to package to get symmetry with the show.py logic
def execute(config, feed, args):
    task_uuids = []
    if args.task_id != None:
        task_uuids += task_ids_to_uuids(config.task_dir, args.task_id)

    if args.task_uuid != None:
        task_uuids += check_task_uuids(config.task_dir, args.task_uuid)
    
    d = tempfile.TemporaryDirectory()
    t = tempfile.NamedTemporaryFile(mode='w+', dir=d.name)
    editor_path = get_editor()
    os.system('{} {}'.format(get_editor(), t.name))
    f = open(t.name, 'rb')
    s = os.stat(t.name)
    t.close()
    logg.debug('file {} {}'.format(t.name, s.st_size))
    if s.st_size == 0:
        logg.error('empty input')
        sys.stderr.write('No input. aborting.\n')
        sys.exit(1)
    content = f.read(s.st_size)
    f.close()

    entry_date = str(email.utils.formatdate())
    subject = args.s
    if subject == None:
        subject = entry_date
    m = EmailMessage()
    m.add_header('Content-Type', 'text/plain')
    m.add_header('Content-Disposition', 'inline')
    m.add_header('Content-Transfer-Encoding', 'base64')
    m.set_param('filename', subject)
    m.set_param('filename', subject, 'Content-Disposition')
    bsf = base64.encodebytes(content)
    m.set_payload(bsf.decode('utf-8'))

    
    mm = MIMEMultipart()
    mm.attach(m)
    mm.add_header('Subject', subject)
    mm.add_header('Date', entry_date)

    entry = feedentry.from_multipart(mm)
    for t in task_uuids:
        uu = feedwarrior.common.parse_uuid(t)
        entry.add_extension(feedwarrior.extension.TASKWARRIOR, uu)

    uu = str(entry.uuid)
    logg.debug('adding entry {}'.format(uu))
    
    fa = fileadapter(config.data_dir, feed.uuid)
    fa.put(entry.uuid, entry, compress=args.z)
   
    feed.add(entry)
