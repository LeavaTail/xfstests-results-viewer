"""generate the instance for some class

This modules define the method to create the some instances
"""

import sys
from logging import getLogger, CRITICAL
from xfstests_results_viewer.testcase import PassedClass, SkippedClass, FailedClass

logger = getLogger("__main__").getChild("generator")

def read_results(directory):
    """Create the list of TestClass instance.

    This method uses "check.log" that is the xfstests result file, and
    categorize as "Passed", "Skipped" and "Failed" testcase. However,
    the instance doesn't include the details xfstests logs.
    (e.g. Cause of skip, timestamp)

    Note:
        Only obtain the log in last result
    """
    testlist = []
    formattedlist = {}
    passedlist = []
    skippedlist = []
    failedlist = []

    try:
        with open('%s/check.log' % (directory), 'r') as f:
            logs = f.read()
    except OSError:
        logger.error("Could not open file under " + directory)
        sys.exit()

    # Obtain from last log
    testlog = logs.split('\n\n')[-1]

    if testlog:
        # test logs are divided into 3 sections
        # 1. Ran (All testcases)
        # 2. Not run (Skipped testcases)
        # 3. Failures: (Failed testcases)
        alltest = testlog.split('\n')[1]
        skippedtest = testlog.split('\n')[2]
        failedtest = testlog.split('\n')[3]

        # test is separated by a space
        testlist = alltest.split(' ')

    # First argument is index 'Ran:' should be skipped
    for test in testlist[1:-1]:
        if test in skippedtest:
            testclass = SkippedClass
            testlist = skippedlist
            logger.debug('%s: Skipped' % (test))
        elif test in failedtest:
            testclass = FailedClass
            testlist = failedlist
            logger.debug('%s: Failed' % (test))
        else:
            testclass = PassedClass
            testlist = passedlist
            logger.debug('%s: Passed' % (test))

        # create instance and append to target list
        t = testclass(test, 0, '', '%s/%s' % (directory, test))
        t.update_time(directory)
        t.update_summary(directory)
        testlist.append(t)

    formattedlist["passed"] = passedlist
    formattedlist["failed"] = failedlist
    formattedlist["skipped"] = skippedlist

    return formattedlist
