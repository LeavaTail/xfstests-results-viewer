#!/usr/bin/env python3
# coding: utf-8
"""organize the xfstests result

This modules analyze and format the xfstests results. This use timestamp and
logfile as well as result directory. As a result, return the lists that is
formatted by JSON.

Example:

    $ python3 analyzer.py /xfstests/results
"""

import os
import sys
import argparse
import re
from logging import getLogger, StreamHandler, DEBUG, INFO, ERROR

import testcase
from conv_json import ConvJsonClass

logger = getLogger(__name__)
handler = StreamHandler()

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
        with open(directory + '/check.log', 'r') as f:
            logs = f.read()
        with open(directory + '/check.time', 'r') as f:
            time = f.read()
    except OSError:
        print("Could not open file under " + directory)
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


    logger.debug('[Initialization]')
    # First argument is index 'Ran:' should be skipped
    for test in testlist[1:-1]:
        if test in skippedtest:
            s = testcase.SkippedClass(test)
            update_details(s, time, directory)
            skippedlist.append(s)
            logger.debug(test + ' :Skipped')
        elif test in failedtest:
            f = testcase.FailedClass(test)
            update_details(f, time, directory)
            failedlist.append(f)
            logger.debug(test + ' :Failed')
        else:
            p = testcase.PassedClass(test)
            update_details(p, time, directory)
            passedlist.append(p)
            logger.debug(test + ' :Passed')
    logger.debug('')

    formattedlist["passed"] = passedlist
    formattedlist["failed"] = failedlist
    formattedlist["skipped"] = skippedlist

    return formattedlist

def update_details(testcase, time, directory):
    testcase.update_summary(directory + '/')
    testcase.update_path(directory)

    # timestamp is separated by a space
    line = re.findall(testcase.name + ' ' + '\d+', time)
    # passed testcase
    if line:
        testcase.update_time(line[0].split(' ')[1])
    # skipped or failed testcase
    else:
        pass

def set_logger(opts):
    """Set the parameter in logger.

    This module set the logger based on the mode that is "Default",
    "Verbose mode" and "Quite mode".
    """
    # Set the log level
    if (opts.verbose):
        level = DEBUG
    elif (opts.quite):
        level = ERROR
    else:
        level = INFO

    handler.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False

    return level

def get_opts():
    """Analyze the command line argument.

    This module can set the parameter by command line argument.
      -o, --output: The strategy in output
      -q, --quite: Restrict the message
      -v, --verbose: Output debug message
    """

    parser = argparse.ArgumentParser(
        prog='xfstests-test-analyzer',
        description='Output json file from xfstests result')

    parser.add_argument('results', help='xfstests results directory path')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-q', '--quite', help='Quite mode', action='store_true')
    parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')
    opts = parser.parse_args()

    return opts

def main():
    output = None
    conv = ConvJsonClass()
    opts = get_opts()
    if opts.output:
        output = open(opts.output, 'a+')

    level = set_logger(opts)
    formattedlist = read_results(opts.results)

    logger.debug('[Result]')
    conv.dump_results(formattedlist, output)
    logger.debug('')

    if output:
        output.close()

if __name__ == "__main__":
    main()
