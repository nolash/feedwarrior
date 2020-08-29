# standard imports
import uuid
import hashlib
import logging

# third-party imports
import tasklib

logg = logging.getLogger(__file__)

defaulthashers = [hashlib.sha256, hashlib.sha1]


def parse_uuid(uu):
    if type(uu).__name__ == 'str':
        return uuid.UUID('urn:uuid:' + uu)
    elif type(uu).__name__ == 'UUID':
        return uu
    raise ValueError('invalid uuid')


def task_ids_to_uuids(task_path, task_ids):
    task_uuids = []
    tw = tasklib.TaskWarrior(task_path)
    for task_id in task_ids:
        # third-party imports
        t = tw.tasks.pending().get(id=task_id)
        task_uuid = t['uuid']
        logg.debug('resolved task uuid {} for id {}'.format(task_uuid, task_id))
        task_uuids.append(task_uuid)
    return task_uuids


def check_task_uuids(task_path, task_uuids):
    task_ok_uuids = []
    tw = tasklib.TaskWarrior(task_path)
    for task_uuid in task_uuids:
        t = tw.tasks.pending().get(uuid=task_uuid)
        task_uuid = t['uuid']
        logg.debug('verified task uuid {}'.format(task_uuid))
        task_ok_uuids.append(task_uuid)
    return task_ok_uuids


