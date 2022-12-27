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

directory = '.'
level = INFO
logger = getLogger(__name__)
handler = StreamHandler()
formattedlist = []

def create_instance():
    """Create the list of TestClass instance.

    This method uses "check.log" that is the xfstests result file, and
    categorize as "Passed", "Skipped" and "Failed" testcase. However,
    the instance doesn't include the details xfstests logs.
    (e.g. Cause of skip, timestamp)

    Note:
        Only obtain the log in last result 
    """

    result_file = directory + '/' + 'check.log'

    try:
        with open(result_file, 'r') as f:
            contents = f.read()
    except OSError:
        print("Could not open file:" + result_file)
        sys.exit()

    # Obtain from last log
    testlog = contents.split('\n\n')[-1]

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
            formattedlist.append(testcase.SkippedClass(test))
            logger.debug(test + ' :Skipped')
        elif test in failedtest:
            formattedlist.append(testcase.FailedClass(test))
            logger.debug(test + ' :Failed')
        else:
            formattedlist.append(testcase.PassedClass(test))
            logger.debug(test + ' :Passed')
    logger.debug('')

def update_time():
    """Update these instance for timestamp.

    This method uses "check.time" that is the xfstests timestamp file.
    """

    result_file = directory + '/' + 'check.time'

    try:
        with open(result_file, 'r') as f:
            contents = f.read()
    except OSError:
        print("Could not open file:" + result_file)
        sys.exit()

    # test is separated by a new line
    for item in formattedlist:
        # timestamp is separated by a space
        line = re.findall(item.name + ' ' + '\d+', contents)
        # passed testcase
        if line:
            item.update_time(line[0].split(' ')[1])
        # skipped or failed testcase
        else:
            pass

def update_summary():
    """Update these instance for details.

    This method uses the result directory that recorded by xfstests.
    """
    for test in formattedlist:
        test.update_summary(directory + '/')

def update_pathname():
    """Update these instance for pathname.

    This method uses the result directory that recorded by xfstests.
    """
    for test in formattedlist:
        test.update_path(directory)

def read_results():
    """Analyze test result and create the TestClass instance.

    This method prepared to visualize the test results. The list formatted
    test results by execute this.
    """

    formattedlist = create_instance()
    update_time()
    update_summary()
    update_pathname()

def set_logger():
    """Set the parameter in logger.

    This module set the logger based on the mode that is "Default",
    "Verbose mode" and "Quite mode".
    """

    handler.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False

def set_params(opts):
    """Set the parameter for this module.

    This module can set the parameter by command line argument.
    The log level is set by verbose or quite mode. The output
    strategy is set by output. The input directory is set by
    results.
    """

    global level
    global output
    global directory

    # Set the log level
    if (opts.verbose):
        level = DEBUG
    elif (opts.quite):
        level = ERROR
    set_logger()

    # Set the output strategy
    if (opts.output):
        sys.stdout = opts.output

    # Set the input directory
    if (opts.results):
        directory = opts.results

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
    opts = get_opts()
    set_params(opts)
    read_results()

    logger.debug('[Result]')
    for test in formattedlist:
        print(test.convert_json())
    logger.debug('')

if __name__ == "__main__":
    main()
