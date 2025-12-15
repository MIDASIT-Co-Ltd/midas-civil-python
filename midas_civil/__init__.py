import requests
from colorama import Fore,Style
from ._mapi import NX,MidasAPI,MAPI_KEY,MAPI_BASEURL,MAPI_COUNTRY,Midas_help
_version_ = "1.2.8"


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


from ._model import Model
from ._boundary import Boundary
from ._utils import getID,getNodeID,utils
from ._node import Node,nodeByID,closestNode,NodeLocalAxis,nodesInRadius
from ._element import Element,elemByID  #Revise
from ._load import Load,Load_Case   # Revise it
from ._group import nodesInGroup,elemsInGroup,Group
from ._loadcomb import LoadCombination


from ._material import Material,CompStrength,CreepShrinkage,TDMatLink

from ._section import Section,Offset

from ._construction import CS
from ._thickness import Thickness
from ._temperature import Temperature # dueto LoadCase

from ._tendon import Tendon
from ._view import View,ResultGraphic,Image

from ._movingload import MovingLoad
from ._settlement import Settlement
from ._analysiscontrol import AnalysisControl
from ._BoundaryChangeAssignment import BoundaryChangeAssignment         # <=== NEEDS A REVIEW (UNNECESSARY CALL)

from ._result_test import Result  #Too much time taken here

