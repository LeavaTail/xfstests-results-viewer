# xfstests-results-viewer

[![Unit test](https://github.com/LeavaTail/sandbox/actions/workflows/unittest.yml/badge.svg)](https://github.com/LeavaTail/sandbox/actions/workflows/unittest.yml)
[![codecov](https://codecov.io/gh/LeavaTail/xfstests-results-viewer/branch/main/graph/badge.svg)](https://codecov.io/gh/LeavaTail/xfstests-results-viewer)

xfstests-results-viewer is a utilities to visutalize the results of
[xfstests](https://git.kernel.org/pub/scm/fs/xfs/xfstests-dev.git).

## Introduction

xfstests is one of the regression test suite for filesystem.
Some developer used this, and confirm the results of xfstests.
However, this is very costly for developer as there are a lot of testcases.

xfstests-results-viewer helps us in initial verification.

This utilities collects test results and output a brief summary as JSON format
(or Excel sheet).
This brief summary doesn't have much information, however it's easy to confirm.

If there are any items that need to confirm in details, developer can follow
the original logs via a link.

## Install

Install from GitHub repository directly with pip command.

```sh
pip install git+https://github.com/LeavaTail/xfstests-results-viewer.git
```

## Usage

Consider the following case
(The test results are stored at `/var/lib/xfstests/results`)

```sh
ls /var/lib/xfstests/results
f2fs  generic  shared  check.log  check.time
```

Pass test results directory as an argument.

```sh
xfstests-results-viewer /var/lib/xfstests/results
```

The brief summary is output to `output.json` in current directory.
(you can change the output destination by `-o` option)

See the help(`-v` option) if you want more.

## License

[GPL-2.0 license](LICENSE)

## Authors

[LeavaTail](https://github.com/LeavaTail)
