# standard imports
import os
import unittest
import tempfile
import logging
import uuid
import shutil
from email.message import EmailMessage

# local imports
from feedwarrior.adapters.fileadapter import fileadapter
from feedwarrior.entry import entry

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestFileadapter(unittest.TestCase):
    
    def setUp(self):
        uu = uuid.uuid4()
        self.feed_uuid = uu
        self.path = tempfile.mkdtemp()


    def tearDown(self):
        shutil.rmtree(self.path)


    def test_put(self):
        a = fileadapter(self.path, self.feed_uuid)
        uu = uuid.uuid4()

        msg = EmailMessage()
        msg.add_header('Date', 'Thu, 2 Jul 2020 12:00:58 +0200')
        msg.add_header('Content-Type', 'multipart/mixed')
        msg.add_attachment('foo')

        e = entry(uu, msg)
        a.put(uu, e)

        print('ieeeee')
        logg.debug(a.get(uu))

if __name__ == '__main__':
    unittest.main()
