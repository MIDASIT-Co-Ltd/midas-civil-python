
from ._mapi import NX,_sumit_req
import sys
import importlib
import itertools
from typing import TYPE_CHECKING , Union
from functools import partial, wraps
from copy import deepcopy
import time

MAX_COPIES = 100                        # slots 0..49, then wraps to 0
_slots = itertools.cycle(range(MAX_COPIES))

def _purge(alias):
    """Drop alias and every alias.* submodule from sys.modules."""
    prefix = alias + "."
    for name in [n for n in sys.modules if n == alias or n.startswith(prefix)]:
        del sys.modules[name]


def _importLIB_SS(pkg_name):
    """Load pkg_name under a recycled unique name, so each copy has its own
    class/global state, including for imports deferred inside functions."""
    alias = f"{pkg_name}_SS{next(_slots)}"
    _purge(alias)                      # free the slot before reusing it
    # print(f" ------------>>   LOADING {pkg_name} LIBRARY AS {alias}")

    spec = importlib.util.find_spec(pkg_name)

    iso_spec = importlib.util.spec_from_file_location(
        alias,
        spec.origin,
        submodule_search_locations=list(spec.submodule_search_locations or []),
    )

    module = importlib.util.module_from_spec(iso_spec)
    sys.modules[alias] = module        # must be set *before* exec_module

    try:
        # print("Step A")
        iso_spec.loader.exec_module(module)
        # print("Step B")
    except BaseException:
        _purge(alias)
        raise
    # print(f"   ✅   LOADED {pkg_name} LIBRARY AS {module.__name__}   ✅    ")
    return module



from typing import Literal
_rType = Literal["MAPI_KEY","PY_LIB",None]
_modelData = Literal["Node","Element","Section","Material"]

class cvl_lib:
    """Copy of the midas_civil library with extra helper functions."""

    @staticmethod
    def replaceData(source,data:_modelData='Node',__dest__=None):
        """
        Clear the current data and replaces with source model data
        """
        
        # print("DEST->",_dest,"\nSOURCE->",source,"\nDATA->",data)
        # -------   NODE  -------
        if data == 'Node':
            __dest__.Node.nodes = deepcopy(source.Node.nodes)
            __dest__.Node.ids = deepcopy(source.Node.ids)
            __dest__.Node.maxID = deepcopy(source.Node.maxID)
            __dest__.Node.Grid = deepcopy(source.Node.Grid)
            __dest__.Node.__nodeDic__ = deepcopy(source.Node.__nodeDic__)
            __dest__.Node.__idIndex__ = deepcopy(source.Node.__idIndex__)
        elif data == 'Element':
            __dest__.Element.elements = deepcopy(source.Element.elements)
            __dest__.Element.ids = deepcopy(source.Element.ids)
            __dest__.Element.maxID = deepcopy(source.Element.maxID)
            __dest__.Element.__elemDIC__ = deepcopy(source.Element.__elemDIC__)
            __dest__.Element.Grid = deepcopy(source.Element.Grid)
        elif data == 'Material':
            __dest__.Material.mats = deepcopy(source.Material.mats)
            __dest__.Material.ids = deepcopy(source.Material.ids)
            __dest__.Material._dic = deepcopy(source.Material._dic)
        elif data == 'Section':
            __dest__.Section.sect = deepcopy(source.Section.sect)
            __dest__.Section.ids = deepcopy(source.Section.ids)
            __dest__.Section._dic = deepcopy(source.Section._dic)
        else:
            raise ValueError(f"replaceData: unsupported data {data!r}. Use 'Node', 'Element', 'Material' or 'Section'.")

    @staticmethod
    def mergeData(source,data:_modelData='Node',__dest__=None):
        """
        Merges the model data (ID increment is to be handled by user)
        """
        
        # print("DEST->",_dest,"\nSOURCE->",source,"\nDATA->",data)
        # -------   NODE  -------
        if data == 'Node':
            for node in source.Node.nodes:
                __dest__.Node(node.X,node.Y,node.Z,node.ID,'',False)
        elif data == 'Element':
            for elm in source.Element.elements:
                elm._GROUP = ''
                __dest__._ADD_ELEM(elm)
        else:
            raise ValueError(f"mergeData: unsupported data {data!r}. Use 'Node', 'Element', 'Material' or 'Section'.")


    @staticmethod
    def shutDown(__dest__=None):
        ''' Closes the launched CIVIL NX instance.'''
        print("     CLOSING CIVIL NX....")


        # # APPROACH A - through API
        # import requests
        # mapi_key = __dest__.MAPI_KEY.data
        # cmdURL = __dest__.MAPI_BASEURL.baseURL + "/doc/EXIT"
        # headers = {
        #                 "Content-Type": "application/json",
        #                 "MAPI-Key": mapi_key
        #             }

        # try:
        #     requests.post(url=cmdURL, headers=headers , json={"Argument":{}},timeout=1)   # Excepting the timeout error
        # except:
        #     pass


        # APPROACH B - through process
        time.sleep(1)
        _Process = __dest__.NX._NX_PROCESS
        _Process.terminate()

        __dest__.Model.clear()
        _purge(__dest__.__name__)
                    


def MIDAS_Model(MAPI_Key=None,bAutoURL=True):
    ''' Return isolated python midas model object.     
    Useful when working with multiple CIVIL NX with different MAPI keys in a single python code.      
    bAutoURL = Automatically obtains the Base URL based on MAPI Key
    
    '''
    if TYPE_CHECKING:
        import midas_civil as CVL_LIB       # seen only by the IDE / type checker
    else:
        CVL_LIB = _importLIB_SS('midas_civil')  # what actually runs

    
    CVL_LIB.Model.clear()

    if MAPI_Key is not None:
        CVL_LIB.MAPI_KEY(MAPI_Key)
        if bAutoURL:
            CVL_LIB.MAPI_BASEURL.autoURL()


    # MANUALLY MAPPING THE CURRENT OPTIONS
    CVL_LIB.NX.SHOW_OUPTUT_IN_TERMINAL = NX.SHOW_OUPTUT_IN_TERMINAL
    CVL_LIB.NX.SYS_EXIT_ON_ERROR = NX.SYS_EXIT_ON_ERROR
    CVL_LIB.NX.OFFLINE = NX.OFFLINE


    # Adding new functions
    setattr(CVL_LIB, "replaceData", partial(cvl_lib.replaceData, __dest__=CVL_LIB))
    setattr(CVL_LIB, "mergeData", partial(cvl_lib.mergeData, __dest__=CVL_LIB))

    _dummyCHECK = True
    if _dummyCHECK:
        return CVL_LIB
    else:
        return cvl_lib


def LaunchNX(bNewMAPIKey=True,returnType:_rType='PY_LIB',NX_exePath:str=None):
    '''
    **THIS FEATURE REQQUIRES ADMIN ACCESS TO MODIFY THE REGISTRY AND LAUNCH CIVIL NX APPLICATION.**       
    Launches a CIVIL/GEN NX instance.    
    The location of EXE file is taken from Registry automatically.    

    bNewMAPIKey = True => NX will be launched with a new MAPI key. When launching multiple instances, this must be True, else connection will fail in second and next instances.    
    returnType = 'PY_LIB' or 'MAPI_KEY'. If the user only wants the updated mapiKey for the NX instance. PY_LIB returns midas model object connected to the launched instance.    
    NX_exePath = Location of application. If version to be used for API is different that default version.   
    
    '''
    try:import winreg
    except:
        print("The command in meant to be used with Admin privilages")
        if NX.SYS_EXIT_ON_ERROR: sys.exit(0)

    # READ FROM REGISTRY ---------

    # MAPI KEY DETAILS
    key_path = f"Software\\MIDAS\\CVLwNX_US\\CONNECTION"  
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)

    url_reg = winreg.QueryValueEx(registry_key, "URI")
    url_reg_key = url_reg[0]

    port_reg = winreg.QueryValueEx(registry_key, "PORT")
    port_reg_key = port_reg[0]

    mapi_reg = winreg.QueryValueEx(registry_key, "Key")
    mapi_key = str(mapi_reg[0])

    startup_orig = 0

    try:
        startup_reg = winreg.QueryValueEx(registry_key, "STARTUP")
        startup_orig = startup_reg[0]
    except: pass


    # PRINT DATA
    # NX.box_print(f'MAPI KEY = {mapi_key}\n STARTUP = {startup_orig}')

    base_url = f'https://{url_reg_key}:{port_reg_key}/civil'
    url = base_url + "/config/ver"

    headers = {"Content-Type": "application/json","MAPI-Key": mapi_key}

    if NX.USER_ID is None:
    # GET THE USER ID -=
        resp = _sumit_req.get(url="https://moa-engineers.midasit.com/mapikey/verify", headers=headers)
        NX.USER_ID = resp.json()['user']
   

    final_mapi_key = mapi_key

    # GET THE UPDATED MAPI KEY
    resp = _sumit_req.post(url="https://moa-engineers.midasit.com/openws/civil",json={'user':NX.USER_ID})
    updated_mapi_key = resp.json()['key']

    if bNewMAPIKey:
        # EDIT REGISTRY (UPDATE THE KEY)-----------------
        key_path = "Software\\MIDAS\\CVLwNX_US\\CONNECTION"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,key_path, 0, winreg.KEY_SET_VALUE) as registry_key:
            winreg.SetValueEx(registry_key, "Key", 0, winreg.REG_SZ, updated_mapi_key)
            winreg.SetValueEx(registry_key, "STARTUP", 0, winreg.REG_DWORD, 1)
        
        final_mapi_key = updated_mapi_key
        # PRINT DATA
        # NX.box_print(f'MAPI KEY = {final_mapi_key}\n STARTUP = {startup_orig}')
    else:
        key_path = "Software\\MIDAS\\CVLwNX_US\\CONNECTION"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,key_path, 0, winreg.KEY_SET_VALUE) as registry_key:
            winreg.SetValueEx(registry_key, "STARTUP", 0, winreg.REG_DWORD, 1)


    # LAUNCHING THE CIVIL NX ----------------------------------------

    headers = {"Content-Type": "application/json","MAPI-Key": final_mapi_key}


    # ----------------------  CIVIL NX LAUNCH PATH -----------------------------
    if NX_exePath is None:
        key_path = f"Software\\MIDAS\\CVLwNX_US\\PATH"  
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        ins_path = winreg.QueryValueEx(registry_key, "Installed Path")
        civilNX_path = ins_path[0]
    else:
        civilNX_path = NX_exePath

    import subprocess
    print(f"     Launching {NX.PRODUCT} NX ",end=" ",flush=True)
    _NX_PROCESS = subprocess.Popen([civilNX_path])
    # ---------------------------------------------------------------------------
    time.sleep(6)   # Initial time gap
    status_open = 'progress'
    counter = 0
    while True:
        response = _sumit_req.get(url=url, headers=headers)
        if response.status_code == 200:
            status_open = 'success'
            break
        time.sleep(1)
        counter+=1
        if counter > 10:
            status_open = 'timeout'
            break
        print("..",end="",flush=True)
    if status_open == 'success': print("   Connected to API  🟢")
    elif status_open == 'timeout': print("   Process timeout  ⚠️")
    else: print("   Unknown error  ❌")

    #---------------------------------------------------------------------

    # Reset MAPI Key and startup to original values
    key_path = "Software\\MIDAS\\CVLwNX_US\\CONNECTION"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,key_path, 0, winreg.KEY_SET_VALUE) as registry_key:
        winreg.SetValueEx(registry_key, "Key", 0, winreg.REG_SZ, mapi_key)
        winreg.SetValueEx(registry_key, "STARTUP", 0, winreg.REG_DWORD, startup_orig)

    if returnType == 'PY_LIB': 
        # import midas_civil as CVL_LIB
        if TYPE_CHECKING:
            import midas_civil as CVL_LIB       # seen only by the IDE / type checker
        else:
            CVL_LIB = _importLIB_SS('midas_civil')  # what actually runs

        # CVL_LIB = CVLLib(_importLIB_SS('midas_civil'))  # what actually runs
        
        CVL_LIB.MAPI_KEY(final_mapi_key)
        CVL_LIB.MAPI_BASEURL.autoURL()
        CVL_LIB.Model.clear()
        CVL_LIB.NX._NX_PROCESS = _NX_PROCESS

        # MANUALLY MAPPING THE CURRENT OPTIONS
        CVL_LIB.NX.SHOW_OUPTUT_IN_TERMINAL = NX.SHOW_OUPTUT_IN_TERMINAL
        CVL_LIB.NX.SYS_EXIT_ON_ERROR = NX.SYS_EXIT_ON_ERROR
        CVL_LIB.NX.OFFLINE = NX.OFFLINE

        # Adding new functions
        setattr(CVL_LIB, "replaceData", partial(cvl_lib.replaceData, __dest__=CVL_LIB))
        setattr(CVL_LIB, "mergeData", partial(cvl_lib.mergeData, __dest__=CVL_LIB))
        setattr(CVL_LIB, "shutDown", partial(cvl_lib.shutDown, __dest__=CVL_LIB))

        return CVL_LIB
    elif returnType == 'MAPI_KEY': 
        return final_mapi_key
    else:
        return cvl_lib
