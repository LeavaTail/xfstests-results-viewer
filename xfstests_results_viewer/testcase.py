"""xfstests result information

This modules stored the xfstests results information. This information use
timestamp and logfile as well as result directory.
"""

import sys
import re
from logging import getLogger
import dataclasses

logger = getLogger("__main__").getChild("testcase")

@dataclasses.dataclass
class TestClass():
    name: str
    sec: int
    path: str
    remarks: str
    """Test result generic class

    The generic class to store xfstests result

    Args:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result

    Attributes:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result
    """

    def __init__(self, name='', sec=0, remarks='', path=''):
        self.name = name
        self.sec = sec
        self.remarks = remarks
        self.path = path

    def update_time(self, timepath):
        pass

    def update_summary(self, pathname):
        pass


class PassedClass(TestClass):
    """Passed result class

    The class to store passed xfstests result

    Args:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result

    Attributes:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result
    """


    def __init__(self, name='', sec=0, remarks='', path=''):
        super().__init__(name, sec, remarks, path)

    def update_time(self, pathname):
        timepath = '%s/check.time' % (pathname)
        try:
            with open(timepath, 'r') as f:
                contents = f.read()
        except OSError:
            logger.error("Could not open file: %s" % (timepath))
            sys.exit()
        # check.time format is "${testname} ${second}"
        line = re.findall('%s \d+' % (self.name), contents)
        try:
            self.sec = int(line[0].split(' ')[1])
        except:
            logger.warning('%d is not recorded at %s' % (self.sec, timepath))


class SkippedClass(TestClass):
    """Skipped result class

    The class to store skipped xfstests result

    Args:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result

    Attributes:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result
    """

    def __init__(self, name='', sec=0, remarks='', path=''):
        super().__init__(name, sec, remarks, path)

    def update_summary(self, pathname):
        logpath = '%s/%s.notrun' % (pathname, self.name)
        try:
            with open(logpath, 'r') as f:
                contents = f.read()
        except OSError:
            logger.error("Could not open file: %s" %(logpath))
            sys.exit()
        self.remarks = contents


class FailedClass(TestClass):
    """Failed result class

    The class to store failed xfstests result

    Args:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result

    Attributes:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result
    """

    def __init__(self, name='', sec=0, remarks='', path=''):
        super().__init__(name, sec, remarks, path)
