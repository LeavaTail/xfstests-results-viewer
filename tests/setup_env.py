"""The Utility for xfstests logfile 

xfstests-results-viewer needs input (xfstests results directory)
This support some operation to prepare environment.
"""

import os
from viewer.testcase import PassedClass, SkippedClass, FailedClass

def create_timefile(basepath, l, t):
    """Create check.time for test

    xfstests records the execution time(sec) to check.time.
    This method prepare this file.

    Args:
        basepath (str): basepath in result directory
        l (list[src]): test name list
        t (list[int]): execution time list
    """
    with open(basepath + '/check.time', mode='x') as f:
        for (x, y) in zip(l, t):
            f.write(x + ' ' + str(y) + '\n')

def create_logfile(basepath, passed, skipped, failed):
    """Create check.log for test

    xfstests records the test report to check.log.
    This method prepare this file.

    Args:
        basepath (str): basepath in result directory
        passed (list[src]): passed test name list
        skipped (list[src]): skipped test name list
        failed (list[src]): failed test name list
    """
    with open(basepath + '/check.log', mode='x') as f:
        f.write('Thu Jan  1 00:00:00 UTC 1970\n')
        write_testline(f, 'Ran: ', passed + skipped + failed)
        write_testline(f, 'Not run: ', skipped)
        write_testline(f, 'Failures: ', failed)
        f.write('Failed ' + str(len(failed)) + ' of ' + str(len(passed + skipped + failed)) + ' tests\n')

def create_notrun(basepath, skipped):
    """Create ${testname}.notrun for test

    xfstests records the summary to ${testname}.notrun if test is skipped.
    This method prepare this file.

    Args:
        basepath (str): basepath in result directory
        skipped (list[src]): skipped test name list

    Note:
        ${testname}.notrun will record testname
    """
    for i in skipped:
        paths = i.rsplit('/', 1)
        os.makedirs(basepath + paths[0], exist_ok=True)
        with open(basepath + i + '.notrun', mode='x') as f:
            f.write(i)

def write_testline(f, msg, l):
    """Helper for xreate_notrun

    Args:
        f (io): io object for result directory
        msg (src): prefix message
        l (list[src]): test name list
    """
    f.write(msg)
    for i in l:
        f.write(i + ' ')
    f.write('\n')
