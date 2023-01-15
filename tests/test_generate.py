"""Unit test for generator.py

testcase class method verification
* read_results() raise exception when check.log is not exist
* read_results() create the dictionary list
"""

import os
import shutil
import pytest
from logging import getLogger, CRITICAL
from tests.setup_env import create_timefile, create_logfile, create_notrun
from xfstests_results_viewer.testcase import PassedClass, SkippedClass, FailedClass
from xfstests_results_viewer.generator import read_results

getLogger("__main__").setLevel(CRITICAL)

# Not exist check.log
def test_nofile(tmpdir):
    d = tmpdir.mkdir("results")
    with pytest.raises(SystemExit):
        read_results(os.path.abspath(d))

# empty test results
def test_emptyfile(tmpdir):
    d = tmpdir.mkdir("results")

    # Create xfstest results files
    create_timefile(d.strpath, [], [])
    create_logfile(d.strpath, [], [], [])
    create_notrun(d.strpath, [])

    # define expected results
    expected = {
        'passed': [],
        'skipped': [],
        'failed': []
    }

    formattedlist = read_results(d.strpath)
    assert formattedlist == expected

# Simple test results
def test_simplefile(tmpdir):
    d = tmpdir.mkdir("results")

    passedlist = ['generic/001']
    skippedlist = ['generic/002']
    failedlist = ['generic/003']
    timelist = [10]

    # Create xfstest results files
    create_timefile(d.strpath, passedlist, timelist)
    create_logfile(d.strpath, passedlist, skippedlist, failedlist)
    create_notrun(d.strpath, skippedlist)

    # define expected results
    expected = {
        'passed': [
            PassedClass(
                passedlist[0],
                timelist[0],
                '',
                '%s/%s' % (d.strpath, passedlist[0])
            )
        ],
        'skipped': [
            SkippedClass(
                skippedlist[0],
                0,
                skippedlist[0],
                '%s/%s' % (d.strpath, skippedlist[0])
            )
        ],
        'failed': [
            FailedClass(
                failedlist[0],
                0,
                '',
                '%s/%s' % (d.strpath, failedlist[0])
            )
        ]
    }

    formattedlist = read_results(d.strpath)
    assert formattedlist == expected
