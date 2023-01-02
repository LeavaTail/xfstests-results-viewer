"""Unit test for testcase.py 

testcase class method verification
* each setter can be set
* lookup *.notrun is success/failed
"""

import os
import unittest
from logging import getLogger, CRITICAL
from analyzer.testcase import PassedClass, SkippedClass, FailedClass

getLogger("__main__").setLevel(CRITICAL)

class TestPassedClass(unittest.TestCase):
    """Unit test for PassedClass

    PassedClass verification
    1. constructor will set `name`
    2. update_time() will set `sec`
    3. update_summary() will be noop
    4. update_path() will be `path` (concatenate basepath to filepath)
    """

    def test_passed1(self):
        target = PassedClass('foo')
        self.assertEqual(target.name, 'foo')

    def test_passed2(self):
        target = PassedClass('foo')
        target.update_time(100)
        self.assertEqual(target.sec, 100)

    def test_passed3(self):
        target = PassedClass('foo')
        target.update_summary('bar')
        self.assertEqual(target.remarks, '')

    def test_passed4(self):
        target = PassedClass('foo')
        target.update_path('path')
        self.assertEqual(target.path, 'path/foo')

class TestSkippedClass(unittest.TestCase):
    """Unit test for SkippedClass

    SkippedClass verification
    1. constructor will set `name`
    2. update_time() will set `sec`
    3. update_summary() will set `remarks` if file is exist
    4. update_summary() will raise SystemExit if file is not exist
    5. update_path() will be `path` (concatenate basepath to filepath)
    """

    base = 'dir'

    @classmethod
    def setUpClass(cls):
        """Prepare the xfstests results directory

        SkippedClass lookup *.notrun file to input the reason why the test
        will be skipped. To verify lookup sequence, create the simple results
        directory. (`dir/foo.notrun`)

        Note:
            That directory and file should be removed after verification
        """
        os.mkdir('dir')
        with open('dir/foo.notrun', mode='x') as f:
            f.write('sample')
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        """Clean up the xfstests results directory

        SkippedClass lookup *.notrun file to input the reason why the test
        will be skipped in setUpClass. these file should be removed after
        verification.
        """
        os.remove('dir/foo.notrun')
        os.rmdir('dir')
        return super().tearDownClass()

    def test_skipped1(self):
        target = SkippedClass('foo')
        self.assertEqual(target.name, 'foo')

    def test_skipped2(self):
        target = SkippedClass('foo')
        target.update_time(100)
        self.assertEqual(target.sec, 100)

    def test_skipped3(self):
        target = SkippedClass('foo')
        target.update_summary('dir/')
        self.assertEqual(target.remarks, 'sample')

    def test_skipped4(self):
        target = SkippedClass('bar')
        with self.assertRaises(SystemExit):
            target.update_summary('dir/')

    def test_skipped5(self):
        target = SkippedClass('foo')
        target.update_path('dir')
        self.assertEqual(target.path, 'dir/foo')

class TestFailedClass(unittest.TestCase):
    """Unit test for FailedClass

    FailedClass verification
    1. constructor will set `name`
    2. update_time() will set `sec`
    3. update_summary() will be noop
    4. update_path() will be `path` (concatenate basepath to filepath)
    """

    def test_failed1(self):
        target = FailedClass('foo')
        self.assertEqual(target.name, 'foo')

    def test_failed2(self):
        target = FailedClass('foo')
        target.update_time(100)
        self.assertEqual(target.sec, 100)

    def test_failed3(self):
        target = FailedClass('foo')
        target.update_summary('bar')
        self.assertEqual(target.remarks, '')

    def test_failed4(self):
        target = FailedClass('foo')
        target.update_path('path')
        self.assertEqual(target.path, 'path/foo')

if __name__ == "__main__":
    unittest.main()
