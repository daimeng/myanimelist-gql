import os.path
from google.appengine.ext import vendor

vendor.add('lib')

PRODUCTION_MODE = not os.environ.get(
    'SERVER_SOFTWARE', 'Development').startswith('Development')
if not PRODUCTION_MODE:
    from google.appengine.tools.devappserver2.python import sandbox
    sandbox._WHITE_LIST_C_MODULES += ['_ctypes', 'gestalt']
    import os
    import sys
    if os.name == 'nt':
        os.name = None
        sys.platform = ''
