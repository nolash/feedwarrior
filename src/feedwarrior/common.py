# standard imports
import uuid

def parse_uuid(uu):
    if type(uu).__name__ == 'str':
        return uuid.UUID('urn:uuid:' + uu)
    elif type(uu).__name__ == 'UUID':
        return uu
    raise ValueError('invalid uuid')
