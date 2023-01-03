"""Unit test for testcase.py 

testcase class method verification
* each setter can be set
* lookup *.notrun is success/failed
"""

import os
import shutil
import pytest
from logging import getLogger, CRITICAL
from tests.setup_env import create_timefile, create_logfile, create_notrun
from viewer.testcase import PassedClass, SkippedClass, FailedClass

getLogger("__main__").setLevel(CRITICAL)

@pytest.fixture(scope='module', autouse=True)
def module_fixture():
    """Prepare the xfstests results directory

    SkippedClass lookup *.notrun file to input the reason why the test
    will be skipped. To verify lookup sequence, create the simple results
    directory. (`dir/foo.notrun`)
    """
    param = {
        'dir': 'dir/',
        'pass': ['generic/001'],
        'skip': ['generic/002'],
        'fail': ['generic/003'],
        'time': [10]
    }
    # Set up tempdir
    os.mkdir(param['dir'])

    # Create xfstest results files
    create_timefile(param['dir'], param['pass'], param['time'])
    create_logfile(param['dir'], param['pass'], param['skip'], param['fail'])
    create_notrun(param['dir'], param['skip'])

    # Main process
    yield param

    # Clean up process
    shutil.rmtree(param['dir'])

# PassedClass constructor will set (default)
def test_passed1(module_fixture):
    param = module_fixture
    target = PassedClass(param['pass'][0])
    assert target.name == param['pass'][0]
    assert target.sec == 0
    assert target.remarks == ''
    assert target.path == ''

# PassedClass constructor will set
def test_passed2(module_fixture):
    param = module_fixture
    target = PassedClass(param['pass'][0], 100, 'foo', 'bar')
    assert target.name == param['pass'][0]
    assert target.sec == 100
    assert target.remarks == 'foo'
    assert target.path == 'bar'

# update_time() will set `sec`
def test_passed3(module_fixture):
    param = module_fixture
    target = PassedClass(param['pass'][0])
    target.update_time(param['dir'])
    assert target.sec == param['time'][0]

# SkippedClass constructor will set (default)
def test_skipped1(module_fixture):
    param = module_fixture
    target = SkippedClass(param['skip'][0])
    assert target.name == param['skip'][0]
    assert target.sec == 0
    assert target.remarks == ''
    assert target.path == ''

# SkippedClass constructor will set
def test_skipped2(module_fixture):
    param = module_fixture
    target = SkippedClass(param['skip'][0], 100, 'foo', 'bar')
    assert target.name == param['skip'][0]
    assert target.sec == 100
    assert target.remarks == 'foo'
    assert target.path == 'bar'

# update_summary will set `remarks`
def test_skipped3(module_fixture):
    param = module_fixture
    target = SkippedClass(param['skip'][0])
    target.update_summary(param['dir'])
    assert target.name == param['skip'][0]
    assert target.sec == 0
    assert target.remarks == param['skip'][0]
    assert target.path == ''

# FailedClass constructor will set (default)
def test_failped1(module_fixture):
    param = module_fixture
    target = FailedClass(param['fail'][0])
    assert target.name == param['fail'][0]
    assert target.sec == 0
    assert target.remarks == ''
    assert target.path == ''

# FailedClass constructor will set
def test_failped2(module_fixture):
    param = module_fixture
    target = FailedClass(param['fail'][0], 100, 'foo', 'bar')
    assert target.name == param['fail'][0]
    assert target.sec == 100
    assert target.remarks == 'foo'
    assert target.path == 'bar'
