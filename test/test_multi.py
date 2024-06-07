# standard imports
import os
import unittest
import tempfile
import logging
import uuid
import shutil

# local imports
from feedwarrior.entry import to_multipart_file
from feedwarrior.entry import from_multipart_file

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestMultipart(unittest.TestCase):
    
    def setUp(self):
        uu = uuid.uuid4()
        self.feed_uuid = uu
        self.path = tempfile.mkdtemp()


    def tearDown(self):
        shutil.rmtree(self.path)


    def test_plain_file(self):
        fp = os.path.join(self.path, 'plain.txt')
        f = open(fp, 'w')
        f.write("foo\nis bar\n")
        f.close()

        fp_multi = to_multipart_file(fp)

        o = from_multipart_file(fp_multi)
        print(o.serialize())


if __name__ == '__main__':
    unittest.main()
