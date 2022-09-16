
from unittest import TestCase
from unittest import mock
from pngquant.pngquant import Pngquant
import base64, os, shutil, tempfile

class PngquantTests(TestCase):
    """
    Test Pngquant.
    """
    def setUp(self):
        self.app = Pngquant()
        self.inputdir = tempfile.mkdtemp()
        self.outputdir = tempfile.mkdtemp()
        self.testpng = 'test.png'
        with open(os.path.join(self.inputdir, self.testpng), 'wb') as fh:
            fh.write(base64.decodebytes(b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVQI12P4DwABAQEAG7buVgAAAABJRU5ErkJggg=='))

    def test_run(self):
        """
        Test the run code.
        """
        args = []
        args.append(self.inputdir)
        args.append(self.outputdir)

        options = self.app.parse_args(args)
        self.assertEqual(options.inputdir, self.inputdir)
        self.assertEqual(options.outputdir, self.outputdir)

        self.app.run(options)

        self.assertTrue(os.path.exists(os.path.join(
            self.outputdir, self.testpng)))

    def tearDown(self):
        shutil.rmtree(self.inputdir)
        shutil.rmtree(self.outputdir)
