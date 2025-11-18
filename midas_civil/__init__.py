import requests
from colorama import Fore,Style
from ._mapi import *
_version_ = "1.1.7"


print('\n╭────────────────────────────────────────────────────────────────────────────────────╮')
print(Style.BRIGHT+f'│                      MIDAS CIVIL-NX PYTHON LIBRARY v{_version_}  🐍                      │')
print('╰────────────────────────────────────────────────────────────────────────────────────╯\n'+Style.RESET_ALL)

if NX.version_check:
    resp =  requests.get("https://pypi.org/pypi/midas_civil/json").json()
    latest_ver =  resp["info"]["version"]
    if _version_ != latest_ver:        
        print(Fore.YELLOW +'╭─ ⚠️   ──────────────────────────────────────────────────────────────────────────────╮')
        print(f"│    Warning: You are using v{_version_}, but the latest available version is v{latest_ver}.      │")
        print(f"│    Run 'pip install midas_civil --upgrade' to update.                              │")
        print('╰────────────────────────────────────────────────────────────────────────────────────╯\n'+Style.RESET_ALL)


from ._model import *
from ._boundary import *
from ._utils import *
from ._node import *
from ._element import *
from ._load import *
from ._group import *
from ._result import *

#--- TESTING IMPORTS ---
from ._material import *

# from ._section import *
from ._section import *

# from ._result_extract import *
from ._construction import *
from ._thickness import *
from ._temperature import *

from ._tendon import *
from ._view import *

from ._movingload import *
from ._settlement import *
from ._analysiscontrol import *
from ._BoundaryChangeAssignment import*

from ._result_test import *

