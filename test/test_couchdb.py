# standard imports
import os
import unittest
import uuid
from email.message import EmailMessage

# third party imports
import pycouchdb

# local imports
from feedwarrior.adapters.couchdbadapter import couchdbadapter
from feedwarrior.entry import entry

DBHOST = os.environ.get('FEEDWARRIOR_HOST', 'localhost')
DBPORT = os.environ.get('FEEDWARRIOR_PORT', 5984)
DBPASS = os.environ.get('FEEDWARRIOR_PASS')
DBUSER = os.environ.get('FEEDWARRIOR_USER')
DBSSL = os.environ.get('FEEDWARRIOR_SSL')

uu = 'x' + uuid.uuid4().hex

class TestCouchdbadapter(unittest.TestCase):

    def setUp(self):
        ssl = DBSSL != None and DBSSL != ''
        scheme = 'http'
        if ssl:
            scheme += 's'
        self.srv = pycouchdb.Server('{}://{}:{}@{}:{}'.format(scheme, DBUSER, DBPASS, DBHOST, DBPORT))
        self.db_name = str(uu)
        self.db = self.srv.create(self.db_name)


    def tearDown(self):
        self.db.cleanup()
        self.srv.delete(self.db_name)


    def test_init(self):
        a = couchdbadapter(DBUSER, DBPASS, self.db_name)


    def test_put(self):
        a = couchdbadapter(DBUSER, DBPASS, self.db_name)
        uu = uuid.uuid4()

        msg = EmailMessage()
        msg.add_header('Date', 'Thu, 2 Jul 2020 12:00:58 +0200')
        msg.add_header('Content-Type', 'multipart/mixed')
        msg.add_attachment('foo')

        e = entry(uu, msg)
        a.put(uu, e)

        a.get(uu)


if __name__ == '__main__':
    unittest.main()
