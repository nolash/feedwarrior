# standard imports
import uuid
import hashlib

defaulthasher = hashlib.sha256

def parse_uuid(uu):
    if type(uu).__name__ == 'str':
        return uuid.UUID('urn:uuid:' + uu)
    elif type(uu).__name__ == 'UUID':
        return uu
    raise ValueError('invalid uuid')
