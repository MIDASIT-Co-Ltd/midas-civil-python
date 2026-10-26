import requests
import sys
from colorama import Fore, Style
try:import winreg
except: pass
import time
from tqdm import tqdm
from typing import Literal
import json
import math

_sumit_req = requests.Session()
# import polars as pl

_httpMethod = Literal["PUT","POST","DELETE","GET"]


# ----------------------------  ERRORS  ------------------------------------------------
class MidasError(Exception):
    """Base class of all errors raised by midas_civil (when NX.SYS_EXIT_ON_ERROR is False)."""

class MidasConnectionError(MidasError):
    """CIVIL NX is not reachable / not connected, or the request timed out."""

class MidasAuthError(MidasError):
    """MAPI key is missing or rejected."""

class MidasAPIError(MidasError):
    """CIVIL NX returned an unusable response (HTTP error with a non-JSON body)."""

class MidasInputError(MidasError, ValueError):
    """Invalid input passed to a midas_civil function."""


def _fail(exc:MidasError):
    """Single exit point for fatal errors.
    NX.SYS_EXIT_ON_ERROR = True  -> stop the script with exit code 1 (non-zero, so CI/automation sees the failure)
    NX.SYS_EXIT_ON_ERROR = False -> raise `exc` so the caller can handle it
    The message is printed only when NX.SHOW_OUPTUT_IN_TERMINAL is True."""
    if NX.SHOW_OUPTUT_IN_TERMINAL:
        tqdm.write(Fore.RED + f" ❌   {exc}" + Style.RESET_ALL)
    if NX.SYS_EXIT_ON_ERROR:
        sys.exit(1)
    raise exc


def _inputError(msg:str):
    """Invalid user input.
    Default mode (SYS_EXIT_ON_ERROR = True): message is printed (if output is enabled) and execution continues as before.
    SYS_EXIT_ON_ERROR = False (caller handles errors): MidasInputError is raised instead of failing silently."""
    if not NX.SYS_EXIT_ON_ERROR:
        raise MidasInputError(msg)
    if NX.SHOW_OUPTUT_IN_TERMINAL:
        print(msg)
_functionMapping = {

'/doc/new' : 'New Project' ,
'/doc/open' : 'Open Project' ,
'/doc/close' : 'Close Project' ,
'/doc/save' : 'Save' ,
'/doc/saveas' : 'Save As' ,
'/doc/stagas' : 'Save Current Stage As' ,
'/doc/import' : 'Import to Json' ,
'/doc/importmxt' : 'Import to mct/mgt' ,
'/doc/export' : 'Export to Json' ,
'/doc/exportmxt' : 'Export to mct/mgt' ,
'/doc/anal' : 'Perform Analysis' ,

'/db/pjcf' : 'Project Information' ,
'/db/unit' : 'Unit System' ,
'/db/styp' : 'Structure Type' ,
'/db/grup' : 'Structure Group' ,
'/db/bngr' : 'Boundary Group' ,
'/db/ldgr' : 'Load Group' ,
'/db/tdgr' : 'Tendon Group' ,

'/db/node' : 'Node' ,
'/db/elem' : 'Element' ,
'/db/skew' : 'Node Local Axis' ,
'/db/mado' : 'Define Domain' ,
'/db/sbdo' : 'Define Sub-Domain' ,
'/db/doel' : 'Domain-Element' ,
'/db/matl' : 'Material Properties' ,
'/db/imfm' : 'Inelastic Material Properties for Fiber Model' ,
'/db/tdmf' : 'Time Dependent Material Properties - User Defined' ,
'/db/tdmt' : 'Time Dependent Material Properties - Creep/Shrinkage' ,
'/db/tdme' : 'Time Dependent Material Properties - Compressive Strength' ,
'/db/edmp' : 'Change Property' ,
'/db/tmat' : 'Time Dependent Material Link' ,
'/db/epmt' : 'Plastic Material' ,
'/db/sect' : 'Section Properties' ,
'/db/thik' : 'Thickness' ,
'/db/tsgr' : 'Tapered Group' ,
'/db/secf' : 'Section Manager - Stiffness' ,
'/db/rpsc' : 'Section Manager - Reinforcements' ,
'/db/strpssm' : 'Section Manager - Stress Points' ,
'/db/pssf' : 'Section Manager - Plate Stiffness Scale Factor' ,
'/db/vbem' : 'Section Manager - Section for Resultant Forces - Virtual Beam' ,
'/db/vsec' : 'Section Manager - Section for Resultant Forces - Virtual Section' ,
'/db/ewsf' : 'Effective Width Scale Factor' ,
'/db/iehc' : 'Inelastic Hinge Control Data' ,
'/db/iehg' : 'Assign Inelastic Hinge Properties' ,
'/db/fimp' : 'Inelastic Material Properties' ,
'/db/fibr' : 'Fiber Division of Section' ,
'/db/grdp' : 'Group Damping' ,
'/db/essf' : 'Element Stiffness Scale Factor' ,

'/db/cons' : 'Supports' ,
'/db/nspr' : 'Point Spring' ,
'/db/gstp' : 'Define General Spring Type' ,
'/db/gspr' : 'Assign General Spring Supports' ,
'/db/ssps' : 'Surface Spring' ,
'/db/elnk' : 'Elastic Link' ,
'/db/rigd' : 'Rigid Link' ,
'/db/nllp' : 'General Link Properties' ,
'/db/nlnk' : 'General Link' ,
'/db/cglp' : 'Change General Link Property' ,
'/db/frls' : 'Beam End Release' ,
'/db/offs' : 'Beam End Offsets' ,
'/db/prls' : 'Plate End Release' ,
'/db/mlfc' : 'Force-Deformation Function' ,
'/db/sdvi' : 'Seismic Device - Viscous Damper/Oil Damper' ,
'/db/sdve' : 'Seismic Device - Viscoelastic Damper' ,
'/db/sdst' : 'Seismic Device - Steel Damper' ,
'/db/sdhy' : 'Seismic Device - Hysteretic Isolator(MSS)' ,
'/db/sdis' : 'Seismic Device - Isolator(MSS)' ,
'/db/mcon' : 'Linear Constraints' ,
'/db/pzef' : 'Panel Zone Effects' ,
'/db/cldr' : 'Define Constraints Label Direction' ,
'/db/drls' : 'Diaphragm Disconnect' ,

'/db/stld' : 'Static Load Cases' ,
'/db/bodf' : 'Self-Weight' ,
'/db/cnld' : 'Nodal Loads' ,
'/db/bmld' : 'Beam Loads' ,
'/db/sdsp' : 'Specified Displacements of Support' ,
'/db/nmas' : 'Nodal Masses' ,
'/db/ltom' : 'Loads to Masses' ,
'/db/nbof' : 'Nodal Body Force' ,
'/db/pslt' : 'Define Pressure Load Type' ,
'/db/pres' : 'Assign Pressure Loads' ,
'/db/pnld' : 'Define Plane Load Type' ,
'/db/pnla' : 'Assign Plane Loads' ,
'/db/fbld' : 'Define Floor Load Type' ,
'/db/fbla' : 'Assign Floor Loads' ,
'/db/fmld' : 'Finishing Material Loads' ,
'/db/posp' : 'Parameter of Soil Properties' ,
'/db/epst' : 'Static Earth Pressure' ,
'/db/epse' : 'Seismic Earth Pressure' ,
'/db/posl' : 'Parameter of Seismic Loads' ,

'/db/etmp' : 'Element Temperature' ,
'/db/gtmp' : 'Temperature Gradient' ,
'/db/btmp' : 'Beam Section Temperature' ,
'/db/stmp' : 'System Temperature' ,
'/db/ntmp' : 'Nodal Temperature' ,

'/db/tdnt' : 'Tendon Property' ,
'/db/tdna' : 'Tendon Profile' ,
'/db/tdcs' : 'Tendon Location for Composite Section' ,
'/db/tdpl' : 'Tendon Prestress' ,
'/db/prst' : 'Prestress Beam Loads' ,
'/db/ptns' : 'Pretension Loads' ,
'/db/exld' : 'External Type Load Case for Pretension' ,
'/db/plcb' : 'Pre-Composite Section' ,

'/db/mvcd' : 'Moving Load Code' ,
'/db/llan' : 'Traffic Line Lanes' ,
'/db/llanch' : 'Traffic Line Lanes - China' ,
'/db/llanid' : 'Traffic Line Lanes - India' ,
'/db/llantr' : 'Traffic Line Lanes - Transverse' ,
'/db/llanop' : 'Traffic Line Lanes - Moving Load Optimizaion' ,
'/db/slan' : 'Traffic Surface Lanes' ,
'/db/slanch' : 'Traffic Surface Lanes - China' ,
'/db/slanop' : 'Traffic Surface Lanes - Moving Load Optimization' ,
'/db/mvhl' : 'Vehicles' ,

'/db/mvhltr' : 'Vehicles - Transverse' ,
'/db/mvld' : 'Moving Load Cases' ,
'/db/mvldch' : 'Moving Load Cases - China' ,
'/db/mvldid' : 'Moving Load Cases - India' ,
'/db/mvldbs' : 'Moving Load Cases - BS' ,
'/db/mvldeu' : 'Moving Load Cases - Eurocode' ,
'/db/mvldpl' : 'Moving Load Cases - Poland' ,
'/db/mvldtr' : 'Moving Load Cases - Transverse' ,
'/db/crgr' : 'Concurrent Reaction Group' ,
'/db/cjfg' : 'Concurrent Joint Force Group' ,
'/db/mvhc' : 'Vehicle Classes' ,
'/db/sinf' : 'Plate Element for Influence Surface' ,
'/db/mlsp' : 'Lane Support - Negative Moments at Interior Piers' ,
'/db/mlsr' : 'Lane Support - Reactions at Interior Piers' ,
'/db/dyla' : 'Dynamic Load Allowance' ,
'/db/impf' : 'Additional Impact Factor' ,
'/db/dyfg' : 'Railway Dynamic Factor' ,
'/db/dynf' : 'Railway Dynamic Factor by Element' ,

'/db/spfc' : 'Response Spectrum Functions - User Type' ,
'/db/splc' : 'Response Spectrum Load Cases' ,
'/db/thgc' : 'Time History Global Control' ,
'/db/this' : 'Time History Load Cases' ,
'/db/thfc' : 'Time History Functions' ,
'/db/thga' : 'Ground Acceleration' ,
'/db/thnl' : 'Dynamic Nodal Loads' ,
'/db/thsl' : 'Time Varying Static Loads' ,
'/db/thms' : 'Multiple Support Excitation' ,

'/db/stag' : 'Define Construction Stage' ,
'/db/cscs' : 'Composite Section for Construction Stage' ,
'/db/tmld' : 'Time Loads for Construction Stage' ,
'/db/stbk' : 'Set-Back Loads for Nonlinear Construction Stage' ,
'/db/cmcs' : 'Camber for Construction Stage' ,
'/db/crpc' : 'Creep Coefficient for Construction Stage' ,

'/db/smpt' : 'Settlement Group' ,
'/db/smlc' : 'Settlement Load Cases' ,

'/db/actl' : 'Main Control Data' ,
'/db/pdel' : 'P-Delta Analysis Control' ,
'/db/buck' : 'Buckling Analysis Control' ,
'/db/eigv' : 'Eigenvalue Analysis Control' ,
'/db/hhct' : 'Heat of Hydration Analysis Control' ,
'/db/mvct' : 'Moving Load Analysis Control' ,
'/db/mvctch' : 'Moving Load Analysis Control - China' ,
'/db/mvctid' : 'Moving Load Analysis Control - India' ,
'/db/mvctbs' : 'Moving Load Analysis Control - BS' ,
'/db/mvcttr' : 'Moving Load Analysis Control - Transverse' ,
'/db/smct' : 'Settlement Analysis Control Data' ,
'/db/nlct' : 'Nonlinear Analysis Control Data' ,
'/db/stct' : 'Construction Stage Analysis Control Data' ,
'/db/bcct' : 'Boundary Change Assignment' ,

'/db/lcom-gen' : 'Load Combinations - General' ,
'/db/lcom-conc' : 'Load Combinations - Concrete Design' ,
'/db/lcom-steel' : 'Load Combinations - Steel Design' ,
'/db/lcom-src' : 'Load Combinations - SRC Design' ,
'/db/lcom-stlcomp' : 'Load Combinations - Composite Steel Girder Design' ,
'/db/lcom-seismic' : 'Load Combinations - Seismic Design' ,
'/db/cutl' : 'Cutting Line' ,
'/db/clwp' : 'Plate Cutting Line Diagram' ,

}


def Midas_help():
    """MIDAS Documnetation : https://midas-rnd.github.io/midasapi-python """
    if NX.SHOW_OUPTUT_IN_TERMINAL:
        print('\n╭────────────────────────────────────────────────────────────────────────────────────╮')
        print("│         HELP MANUAL   :     https://midas-rnd.github.io/midasapi-python/           │")
        print('╰────────────────────────────────────────────────────────────────────────────────────╯\n')



class NX:
    version_check = False    # CHANGE IT TO FALSE TO SKIP VERSION CHECK OF LIBRARY
    user_print = True

    debug_request = False
    debug_requestJSON = False
    debug_response = False

    onlyNode = False
    visualiser = True
    modelIDs = {} # Handles the fast MAX ID
    autoTaperGroup = False
    dispWarning = True
    
    _isSyncUnit = False
    _isSyncNodeElem = False

    PRODUCT = 'CIVIL'
    USER_ID = None
    SOLVER = 'FES'
    _MEC_VERSIONS = ['9.7.5']
    SAVE_DEBUG_LOG = False
    OFFLINE = False     # DISABLE MAPI CALLS
    SEND_IN_CHUNKS = False
    SYS_EXIT_ON_ERROR = True
    SHOW_OUPTUT_IN_TERMINAL = True
    # TIMEOUT = (15, None)    # (connect, read) seconds for every request. Read timeout None = wait for long analyses. eg. NX.TIMEOUT = (15, 600)

    units = {
        "FORCE": "KN",
        "DIST": "M",
        "HEAT": "KJ",
        "TEMPER": "C"
    }



    # Function for quick saving of JSON
    @staticmethod
    def saveJSON(jsonData,fileLocation = "jsData.json"):
        import json
        with open(fileLocation, "w", encoding="utf-8") as f:
            json.dump(jsonData, f, indent=4, ensure_ascii=False)
        return True

    # Function to quickly print text in a box , width -> CENTER Align
    @staticmethod
    def box_print(text:str="HELLO WORLD",width:int=None,pad:int=1,text_col=Fore.WHITE,border_col=Fore.LIGHTWHITE_EX):

        padding = pad

        lines = text.splitlines()

        length = max([len(line) for line in lines])

        if width:
            length = max(length,width)
        leng = length+2*padding


        print(border_col+"╭","─"*leng,"╮",sep="")
        for line in lines:
            if width:
                gap = (leng-len(line))//2
                print("│"," "*gap,text_col+line," "*(leng-len(line)-gap),border_col+"│",sep="")
            else:
                print("│"," "*padding,text_col+line," "*(leng-padding-len(line)),border_col+"│",sep="")
        print("╰","─"*leng,"╯"+Style.RESET_ALL,sep="")

        return True
    
        

class MAPI_COUNTRY:
    
    country = "US"

    def __init__(self,country:str="US"):
        ''' Define Civil NX country to automatically set Base URL and MAPI Key from registry.
        ```
        MAPI_COUNTRY('US') # For english version
        MAPI_COUNTRY('KR') # For Korean version
        MAPI_COUNTRY('CH') # For Chinese version
        ```
        '''
        if country.lower() in ['us','ch','kr','jp']:
            MAPI_COUNTRY.country = country.upper()
        else:
            MAPI_COUNTRY.country = 'US'
        
        MAPI_BASEURL.setURLfromRegistry()
        MAPI_KEY.get_key()  # Intial Key from registry


class MAPI_BASEURL:
    baseURL = "https://moa-engineers.midasit.com:443/civil"
    server_loc = "Global"
    
    def __init__(self, baseURL:str = "https://moa-engineers.midasit.com:443/civil"):
        ''' Define the Base URL for API connection.
        ```
        MAPI_BASEURL('https://moa-engineers.midasit.com:443/civil')
        ```
        '''
        MAPI_BASEURL.baseURL = baseURL
        if MAPI_KEY.count < 0: MAPI_KEY.count = 0     # re-check the connection on the next request

    @classmethod
    def get_url(cls):
        return MAPI_BASEURL.baseURL
    
    @classmethod
    def setURLfromRegistry(cls):
        try:
            key_path = f"Software\\MIDAS\\CVLwNX_{MAPI_COUNTRY.country}\\CONNECTION"  
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            url_reg = winreg.QueryValueEx(registry_key, "URI")
            url_reg_key = url_reg[0]

            port_reg = winreg.QueryValueEx(registry_key, "PORT")
            port_reg_key = port_reg[0]

            url_comb = f'https://{url_reg_key}:{port_reg_key}/civil'

            if NX.SHOW_OUPTUT_IN_TERMINAL: tqdm.write(f' 🌐   BASE URL is taken from Registry entry.  >>  {url_comb}')
            MAPI_BASEURL(url_comb)
        except Exception:
            _fail(MidasConnectionError("BASE URL is not defined. Click on Apps > API Settings to copy the BASE URL Key.\nDefine it using MAPI_BASEURL('https://moa-engineers.midasit.com:443/civil')"))

    @staticmethod
    def autoURL():
        base_urls = [
            "https://moa-engineers-in.midasit.com:443/civil",
            "https://moa-engineers-kr.midasit.com:443/civil",
            "https://moa-engineers-gb.midasit.com:443/civil",
            "https://moa-engineers-us.midasit.com:443/civil",
            "https://moa-engineers.midasit.cn:443/civil"
            ]
        serv_locations = ["INDIA","KOREA","EUROPE","USA","CHINA"]
        mapi_key = MAPI_KEY.get_key()
        chk = 0
        for i,base_url in enumerate(base_urls):
            url = base_url + "/config/ver"
            headers = {
                "Content-Type": "application/json",
                "MAPI-Key": mapi_key
            }
            try:
                response = _sumit_req.get(url=url, headers=headers, timeout=(5, 15))
            except requests.exceptions.RequestException:
                continue        # server not reachable -> try the next one
            if response.status_code == 200:
                MAPI_BASEURL(base_url)
                MAPI_BASEURL.server_loc = serv_locations[i]
                chk=1
                break
        if chk==0:
            _fail(MidasConnectionError("Could not find the BASE URL automatically. Kindly enter it manually using MAPI_BASEURL(...).\nRefer to https://moa.midasit.com/services to find the correct URL."))

class MAPI_KEY:
    """MAPI key from MIDAS CIVIL NX.\n\nEg: MAPI_Key("eadsfjaks568wqehhf.ajkgj345qfhh")"""
    data = ""
    count = 1
    
    def __init__(self, mapi_key:str):
        MAPI_KEY.data = mapi_key
        if MAPI_KEY.count < 0: MAPI_KEY.count = 0     # re-check the connection on the next request

    @classmethod
    def get_key(cls):
        if MAPI_KEY.data == "":
            try:
                key_path = f"Software\\MIDAS\\CVLwNX_{MAPI_COUNTRY.country}\\CONNECTION"
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                value = winreg.QueryValueEx(registry_key, "Key")
                my_key = value[0]
            except Exception:
                _fail(MidasAuthError("MAPI KEY is not defined. Click on Apps > API Settings to copy the MAPI Key.\n Define it using MAPI_KEY('xxxx')"))
            MAPI_KEY(my_key)
            if NX.SHOW_OUPTUT_IN_TERMINAL: tqdm.write(f' 🔑   MAPI-KEY is taken from Registry entry.  >>  {my_key[:6]}...')
        else:
            my_key = MAPI_KEY.data
        
        return my_key
#---------------------------------------------------------------------------------------------------------------

#2 midas API link code:
_MSG_NOT_CONNECTED = ("Civil NX model is not connected.  Click on 'Apps > Connect' in Civil NX.\n"
                      "Make sure the MAPI Key in python code is matching with the MAPI key in Civil NX.")
_MSG_INVALID_KEY = ("MAPI KEY entered is invalid.\n"
                    "Please consider refreshing MAPI-Key in CIVIL NX and resending the request.")

def MidasAPI(method:_httpMethod, command:str, body:dict=None)->dict:
    """Sends HTTP Request to MIDAS CIVIL NX
            Parameters:
                Method: "PUT" , "POST" , "GET" or "DELETE"
                Command: eg. "/db/NODE"
                Body: {{"Assign":{{1{{'X':0, 'Y':0, 'Z':0}}}}}}            
            Examples:
                ```python
                # Create a node
                MidasAPI("PUT","/db/NODE",{{"Assign":{{"1":{{'X':0, 'Y':0, 'Z':0}}}}}})"""
    if body is None:
        body = {}
    if method not in ("PUT","POST","GET","DELETE"):
        raise ValueError(f"Invalid HTTP method {method!r}. Use 'PUT', 'POST', 'GET' or 'DELETE'.")

    if MAPI_KEY.count == 1:
        # ONLY ONE TIME - WHEN API COMMANDS ARE USED
        MAPI_KEY.count = 0

        if NX.OFFLINE and NX.SHOW_OUPTUT_IN_TERMINAL:
            NX.box_print("  OFFLINE MODE ACTIVE  ",pad=30,text_col=Fore.RED,border_col=Fore.RED)

        if NX.SAVE_DEBUG_LOG:
            NX.debug_request = True
            sys.stdout = open("midas_civil_debug_log.txt", "w", encoding="utf-8")

    if NX.OFFLINE:
        return {}

    if MAPI_KEY.count == 0:
        # FIRST REQUEST TO THIS KEY/URL : confirm the connection and detect the product.
        # Runs even when terminal output is disabled (only the banner depends on it).
        MAPI_KEY.count = -1
        try:
            _checkUSER()
        except BaseException:
            MAPI_KEY.count = 0      # check again on the next request
            raise

    headers = {
        "Content-Type": "application/json",
        "MAPI-Key": MAPI_KEY.get_key()
    }

    # IF IT IS A DB TYPE OF JSON WITH ASSIGN ONLY SEND IN CHUNKS
    if NX.SEND_IN_CHUNKS and command.upper().startswith('/DB') and isinstance(body.get("Assign"),dict):
        LIST_KEYS = list(body["Assign"].keys())
        N_REQ = min(_sizeToNumReq(_findSizeJSON(body)), max(len(LIST_KEYS),1))
        MAX_NUM = math.ceil(len(LIST_KEYS)/N_REQ) if LIST_KEYS else 1
        resp, first_error = None, None
        for start in range(0, max(len(LIST_KEYS),1), MAX_NUM):
            json_send = {"Assign":{k:body["Assign"][k] for k in LIST_KEYS[start:start+MAX_NUM]}}
            response = _sendAPI_cmd(method,command,json_send,headers)
            resp = _parseResponse(response,method,command)
            if first_error is None and isinstance(resp,dict) and 'error' in resp:
                first_error = resp
        if first_error is not None:
            resp = first_error      # an error in any chunk is reported, not hidden by later chunks
    else:
        response = _sendAPI_cmd(method,command,body,headers)
        resp = _parseResponse(response,method,command)

    if NX.SHOW_OUPTUT_IN_TERMINAL and NX.dispWarning:
        if isinstance(resp,dict) and 'error' in resp:
            cmd = _functionMapping.get(command.lower(),command)
            try: err_msg = str(resp["error"]["message"])
            except Exception: err_msg = str(resp["error"])
            tqdm.write(f'    ⚠️      Error observed in {cmd}.   |   URL : {command}')
            tqdm.write(f'           Error : {Fore.LIGHTMAGENTA_EX+err_msg+Style.RESET_ALL}\n')        


    return resp


def _parseResponse(response, method, command):
    """Checks the HTTP status of EVERY response and returns the decoded JSON."""
    status = response.status_code
    if status == 401:
        _fail(MidasAuthError(_MSG_INVALID_KEY))
    try:
        resp = response.json()
    except ValueError:
        if status == 404:
            _fail(MidasConnectionError(_MSG_NOT_CONNECTED))
        _fail(MidasAPIError(f"{method} {command} returned HTTP {status} with a non-JSON response: {str(getattr(response,'text',''))[:200]!r}"))
    if status == 404 and command.lower().startswith('/config/ver'):
        _fail(MidasConnectionError(_MSG_NOT_CONNECTED))
    return resp


#--------------------------------------------------------------------

def _getUNIT():
    return MidasAPI('GET','/db/UNIT',{})['UNIT']['1']

def _setUNIT(unitJS):
    js = {
        "Assign" : {
            "1" : unitJS
        }
    }
    MidasAPI('PUT','/db/UNIT',js)


def _checkUSER():
    ''' Detects the connected product (CIVIL / GEN) and solver. Prints the banner only when output is enabled. '''
    response =  MidasAPI('GET','/config/ver',{})
    if isinstance(response,dict) and 'VER' in response:
        resp:dict = response['VER']
        _product = str(resp.get('NAME',''))
        if 'CIVIL' in _product:
            NX.PRODUCT = 'CIVIL'
        elif 'GEN' in _product:
            NX.PRODUCT = 'GEN'
        
        _version = resp.get('VERSION','9.6.0')
        if _version in NX._MEC_VERSIONS:
            NX.SOLVER = 'MEC'

        if not (NX.SHOW_OUPTUT_IN_TERMINAL and NX.user_print):
            return
 

        # print(f"{' '*15}Connected to {resp['NAME']}")
        # print(f"{' '*15}USER : {resp['USER']}          COMPANY : {resp['COMPANY']}")

        ln1 = f"Connected to {resp.get('NAME','')}            SERVER : {MAPI_BASEURL.server_loc}"
        ln2 = f"USER : {resp.get('USER','')}          COMPANY : {resp.get('COMPANY','')}"

        lg_ln1 = 66-len(ln1)
        lg_ln2 = 70-len(ln2)

        line1 = f"│{' '*12} {ln1} {' '*lg_ln1} 🟢 │"
        line2 = f"│{' '*12} {ln2} {' '*lg_ln2}│"
        tqdm.write(Fore.GREEN+'\n╭─ 🔔  ──────────────────────────────────────────────────────────────────────────────╮')
        tqdm.write(line1)
        tqdm.write(line2)
        tqdm.write('╰────────────────────────────────────────────────────────────────────────────────────╯\n'+Style.RESET_ALL)

        if NX.PRODUCT !='CIVIL':
            tqdm.write(Fore.YELLOW +'╭─ ⚠️   ──────────────────────────────────────────────────────────────────────────────╮')
            tqdm.write(f"│      Warning: You are using midas_civil library to connect with GEN NX.            │")
            tqdm.write(f"│      Some GEN NX specific options may not be avaialble.                            │")
            tqdm.write('╰────────────────────────────────────────────────────────────────────────────────────╯\n'+Style.RESET_ALL)


        # print('─'*86)

def _sendAPI_cmd(method, command, body, headers):
    base_url = MAPI_BASEURL.baseURL
    url = base_url + command

    start_time = time.perf_counter()

    try:
        if method == "POST":
            response = _sumit_req.post(url=url, headers=headers, json=body)
        elif method == "PUT":
            response = _sumit_req.put(url=url, headers=headers, json=body)
        elif method == "GET":
            response = _sumit_req.get(url=url, headers=headers)
        elif method == "DELETE":
            response = _sumit_req.delete(url=url, headers=headers)
        else:
            raise ValueError(f"Invalid HTTP method {method!r}. Use 'PUT', 'POST', 'GET' or 'DELETE'.")
    except requests.exceptions.Timeout:
        _fail(MidasConnectionError(f"Request timed out ({method} {command})."))
    except requests.exceptions.ConnectionError as e:
        _fail(MidasConnectionError(f"Could not reach {base_url} ({method} {command}): {e}"))

    
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if NX.SHOW_OUPTUT_IN_TERMINAL and NX.debug_request:
        tqdm.write(Fore.RED+f">>   METHOD : {method} |  URL : {command} | STATUS :  {response.status_code} | TIME : {elapsed_time:.4f} sec "+Style.RESET_ALL)
    if NX.SHOW_OUPTUT_IN_TERMINAL and NX.debug_requestJSON:
        tqdm.write(Fore.CYAN+">>  "+str(body)+Style.RESET_ALL)
    if NX.SHOW_OUPTUT_IN_TERMINAL and NX.debug_response:
        tqdm.write(Fore.GREEN+"<<  "+str(getattr(response,'text',''))+Style.RESET_ALL)

    return response

def _findSizeJSON(data):
    json_bytes = len(json.dumps(data).encode("utf-8"))
    size_mb = json_bytes / (1024 * 1024)
    # print(f"{size_mb:.4f} MB")
    return size_mb

def _sizeToNumReq(size):
    # print("N REQUESTS = ",int(size/7)+1)
    return int(size/7)+1
