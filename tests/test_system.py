"""System test 

testcase class method verification
* verify whether the utility output json file
* verify whether the utility can output excel file
* verify whether the utility can change output path
* verify whether the utility can change logger level
"""

import os
import pytest
from unittest.mock import patch
from logging import getLogger, CRITICAL
from tests.setup_env import create_timefile, create_logfile, create_notrun
from xfstests_results_viewer.__main__ import main

getLogger("__main__").setLevel(CRITICAL)

@pytest.fixture(scope='function', autouse=True)
def module_fixture():
    """Clean up the summary file

    this utility output at current directory.
    Remove the file to decouple dependency between each tests.
    """

    # Set up process

    # Main process
    yield

    # Clean up process
    if(os.path.isfile('out.json')):
        os.remove('out.json')
    if(os.path.isfile('out.xlsx')):
        os.remove('out.xlsx')

# empty results files
def test_default1(tmpdir):
    d = tmpdir.mkdir("results")
    # Create xfstest results files
    create_timefile(d.strpath, [], [])
    create_logfile(d.strpath, [], [], [])
    create_notrun(d.strpath, [])

    # command line arguments
    args = [
        "xfstests_results_viewer",
        d.strpath
    ]

    with patch("sys.argv", args):
        main()
    assert os.path.isfile('out.json') == True

# simple results files
def test_default2(tmpdir):
    d = tmpdir.mkdir("results")

    passedlist = ['generic/001']
    skippedlist = ['generic/002']
    failedlist = ['generic/003']
    timelist = [10]

    # Create xfstest results files
    create_timefile(d.strpath, passedlist, timelist)
    create_logfile(d.strpath, passedlist, skippedlist, failedlist)
    create_notrun(d.strpath, skippedlist)

    # command line arguments
    args = [
        "xfstests_results_viewer",
        d.strpath
    ]

    with patch("sys.argv", args):
        main()
    assert os.path.isfile('out.json') == True

# change output path
def test_output(tmpdir):
    d = tmpdir.mkdir("results")

    # Create xfstest results files
    create_timefile(d.strpath, [], [])
    create_logfile(d.strpath, [], [], [])
    create_notrun(d.strpath, [])

    # command line arguments
    args = [
        "xfstests_results_viewer",
        "-o%s/out.json" % d.strpath,
        d.strpath
    ]

    with patch("sys.argv", args):
        main()
    assert os.path.isfile('%s/out.json' % d.strpath) == True

# excel format
def test_excel(tmpdir):
    d = tmpdir.mkdir("results")

    # Create xfstest results files
    create_timefile(d.strpath, [], [])
    create_logfile(d.strpath, [], [], [])
    create_notrun(d.strpath, [])

    # command line arguments
    args = [
        "xfstests_results_viewer",
        "--format=excel",
        d.strpath
    ]

    with patch("sys.argv", args):
        main()
    assert os.path.isfile('out.xlsx') == True

# verbose mode
def test_verbose(tmpdir):
    d = tmpdir.mkdir("results")

    # Create xfstest results files
    create_timefile(d.strpath, [], [])
    create_logfile(d.strpath, [], [], [])
    create_notrun(d.strpath, [])

    # command line arguments
    args = [
        "xfstests_results_viewer",
        "-v",
        d.strpath
    ]

    with patch("sys.argv", args):
        main()
    assert os.path.isfile('out.json') == True

# quite mode
def test_quite(tmpdir):
    d = tmpdir.mkdir("results")

    # Create xfstest results files
    create_timefile(d.strpath, [], [])
    create_logfile(d.strpath, [], [], [])
    create_notrun(d.strpath, [])

    # command line arguments
    args = [
        "xfstests_results_viewer",
        "-q",
        d.strpath
    ]

    with patch("sys.argv", args):
        main()
    assert os.path.isfile('out.json') == True
