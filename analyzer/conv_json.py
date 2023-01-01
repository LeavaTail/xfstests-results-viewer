"""convert xfstest results to JSON format

This modules define the method for JSON format.
"""

import sys
import json

def convert_results(l):
    """This method convert the list to JSON format

    JSON module can convert the instance to JSON format. however
    it cannot do it as default. The custom default method is defined.
    """
    return json.dumps(l, default=default_method, sort_keys=True, indent=4)

def dump_results(l, output):
    """This method dump the results to JSON format

    Args:
        l (list): The class instance list 
        output (io.TextIOWrapper): Output file (If None, then stdout)

    Examples:
        >>> dump_results({"passed": [testcase.SkippepClass("foo")]}]}, None)
        {
            "passed": [
                {
                    "name": "foo",
                    "path": "",
                    "remarks": "",
                    "sec": 0
                }
            ]
        }

    dump the results converts to JSON format.
    """
    if output is None:
        output = sys.stdout

    output.write(convert_results(l))
    output.write('\n')

def default_method(item):
    if isinstance(item, object) and hasattr(item, '__dict__'):
        return item.__dict__
    else:
        raise TypeError
