"""convert xfstest results to JSON format

This modules define the method for JSON format.
"""

import json

def convert_results(l):
    """This method convert the list to JSON format

    JSON module can convert the instance to JSON format. however
    it cannot do it as default. The custom default method is defined.
    """
    return json.dumps(l, default=default_method, sort_keys=True, indent=4)


def default_method(item):
    if isinstance(item, object) and hasattr(item, '__dict__'):
        return item.__dict__
    else:
        raise TypeError
