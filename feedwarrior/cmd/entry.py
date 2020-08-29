# standard imports
import os
import email
import logging
import uuid
import json
import gzip

# local imports
import feedwarrior
from feedwarrior import entry as feedentry
from feedwarrior.adapters import fileadapter
from feedwarrior.common import task_ids_to_uuids, check_task_uuids

logg = logging.getLogger()


def parse_args(argparser):
    argparser.add_argument('-z', action='store_true', help='compress entry with gzip')
    argparser.add_argument('--task-id', dest='task_id', type=int, action='append', help='add taskwarrior task id relations translated to uuis (cannot be used with --task-uuid')
    argparser.add_argument('--task-uuid', dest='task_uuid', type=str, action='append', help='add taskwarrior task uuid relations (cannot be used with --task-id')
    argparser.add_argument('path', help='multipart file to use for content')
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

    entry = feedentry.from_multipart_file(args.path)
    for t in task_uuids:
        uu = feedwarrior.common.parse_uuid(t)
        entry.add_extension(feedwarrior.extension.TASKWARRIOR, uu)

    uu = str(entry.uuid)
    logg.debug('adding entry {}'.format(uu))
    
    fa = fileadapter(config.data_dir, feed.uuid)
    fa.put(entry.uuid, entry, compress=args.z)
   
    feed.add(entry)
