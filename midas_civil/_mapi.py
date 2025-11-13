import requests
import sys
from colorama import Fore, Style
try:import winreg
except: pass
import time
import polars as pl



def Midas_help():
    """MIDAS Documnetation : https://midas-rnd.github.io/midasapi-python """
    print('\n╭────────────────────────────────────────────────────────────────────────────────────╮')
    print("│         HELP MANUAL   :     https://midas-rnd.github.io/midasapi-python/           │")
    print('╰────────────────────────────────────────────────────────────────────────────────────╯\n')



class NX:
    version_check = True
    user_print = True
    debug_request = False
    debug_requestJSON = False
    debug_response = False
    dummy_elems = False

    _symbol_responseCode_ = {
        "1" : "⌛",
        "2" : "✅",
        "3" : "⚠️",
        "4" : "💀",
        "5" : "💀"
    }


    @staticmethod
    def JSToDF_Results(js_json):
        res_json = {}

        c=0
        for heading in js_json["SS_Table"]["HEAD"]:
            for dat in js_json["SS_Table"]["DATA"]:
                try:
                    res_json[heading].append(dat[c])
                except:
                    res_json[heading]=[]
                    res_json[heading].append(dat[c])

            c+=1

        res_df = pl.DataFrame(res_json)
        return(res_df)
    

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
        
        MAPI_BASEURL.set_url()
        MAPI_KEY.get_key()


class MAPI_BASEURL:
    baseURL = "https://moa-engineers.midasit.com:443/civil"
    
    def __init__(self, baseURL:str = "https://moa-engineers.midasit.com:443/civil"):
        ''' Define the Base URL for API connection.
        ```
        MAPI_BASEURL('https://moa-engineers.midasit.com:443/civil')
        ```
        '''
        MAPI_BASEURL.baseURL = baseURL
        
    @classmethod
    def get_url(cls):
        return MAPI_BASEURL.baseURL
    
    @classmethod
    def set_url(cls):
        try:
            key_path = f"Software\\MIDAS\\CVLwNX_{MAPI_COUNTRY.country}\\CONNECTION"  
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            url_reg = winreg.QueryValueEx(registry_key, "URI")
            url_reg_key = url_reg[0]

            port_reg = winreg.QueryValueEx(registry_key, "PORT")
            port_reg_key = port_reg[0]

            url_comb = f'https://{url_reg_key}:{port_reg_key}/civil'

            print(f' 🌐   BASE URL is taken from Registry entry.  >>  {url_comb}')
            MAPI_BASEURL(url_comb)
        except:
            print(" 🌐   BASE URL is not defined. Click on Apps > API Settings to copy the BASE URL Key.\nDefine it using MAPI_BASEURL('https://moa-engineers.midasit.com:443/civil')")
            sys.exit(0)

class MAPI_KEY:
    """MAPI key from Civil NX.\n\nEg: MAPI_Key("eadsfjaks568wqehhf.ajkgj345qfhh")"""
    data = ""
    count = 1
    
    def __init__(self, mapi_key:str):
        MAPI_KEY.data = mapi_key
        
    @classmethod
    def get_key(cls):
        if MAPI_KEY.data == "":
            try:
                key_path = f"Software\\MIDAS\\CVLwNX_{MAPI_COUNTRY.country}\\CONNECTION"  
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                value = winreg.QueryValueEx(registry_key, "Key")
                my_key = value[0]
                MAPI_KEY(my_key)
                print(f' 🔑   MAPI-KEY is taken from Registry entry.  >>  {my_key[:35]}...')
            except:
                print(f"🔑   MAPI KEY is not defined. Click on Apps > API Settings to copy the MAPI Key.\n Define it using MAPI_KEY('xxxx')")
                sys.exit(0)
        else:
            my_key = MAPI_KEY.data
        
        return my_key
#---------------------------------------------------------------------------------------------------------------

#2 midas API link code:
def MidasAPI(method:str, command:str, body:dict={})->dict:
    """Sends HTTP Request to MIDAS Civil NX
            Parameters:
                Method: "PUT" , "POST" , "GET" or "DELETE"
                Command: eg. "/db/NODE"
                Body: {{"Assign":{{1{{'X':0, 'Y':0, 'Z':0}}}}}}            
            Examples:
                ```python
                # Create a node
                MidasAPI("PUT","/db/NODE",{{"Assign":{{"1":{{'X':0, 'Y':0, 'Z':0}}}}}})"""
    
    base_url = MAPI_BASEURL.baseURL
    mapi_key = MAPI_KEY.get_key()

    url = base_url + command
    headers = {
        "Content-Type": "application/json",
        "MAPI-Key": mapi_key
    }

    if MAPI_KEY.count == 1:
        MAPI_KEY.count =0
        if NX.user_print:
            _checkUSER()




    start_time = time.perf_counter()


    if method == "POST":
        response = requests.post(url=url, headers=headers, json=body)
    elif method == "PUT":
        response = requests.put(url=url, headers=headers, json=body)
    elif method == "GET":
        response = requests.get(url=url, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url=url, headers=headers)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if NX.debug_request:
        # sym = NX._symbol_responseCode_[str(response.status_code)[0]]
        # print(Fore.RED+f">>   METHOD : {method} |  URL : {command} | STATUS : "+Fore.YELLOW+f" {response.status_code} "+Fore.RED+f"| TIME : {elapsed_time:.4f} sec "+Style.RESET_ALL)
        print(Fore.RED+f">>   METHOD : {method} |  URL : {command} | STATUS :  {response.status_code} | TIME : {elapsed_time:.4f} sec "+Style.RESET_ALL)
    if NX.debug_requestJSON:
        print(Fore.CYAN+">>  "+str(body)+Style.RESET_ALL)
    if NX.debug_response:
        print(Fore.GREEN+">>  "+str(response.json())+Style.RESET_ALL)

    if MAPI_KEY.count == 0:
        MAPI_KEY.count = -1
        if response.status_code == 404:
            print(Fore.RED +'\n╭─ 💀   ─────────────────────────────────────────────────────────────────────────────╮')
            print(f"│  Civil NX model is not connected.  Click on 'Apps > Connect' in Civil NX.          │")
            print(f"│  Make sure the MAPI Key in python code is matching with the MAPI key in Civil NX.  │")
            print('╰────────────────────────────────────────────────────────────────────────────────────╯\n'+Style.RESET_ALL)
            sys.exit(0)
    


    return response.json()


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
    try:
        resp =  MidasAPI('GET','/config/ver',{})['VER']

        # print(f"{' '*15}Connected to {resp['NAME']}")
        # print(f"{' '*15}USER : {resp['USER']}          COMPANY : {resp['COMPANY']}")

        ln1 = f"Connected to {resp['NAME']}"
        ln2 = f"USER : {resp['USER']}          COMPANY : {resp['COMPANY']}"

        lg_ln1 = 63-len(ln1)
        lg_ln2 = 67-len(ln2)

        line1 = f"│{' '*15} {ln1} {' '*lg_ln1} 🟢 │"
        line2 = f"│{' '*15} {ln2} {' '*lg_ln2}│"
        print(Fore.GREEN+'\n╭─ 🔔  ──────────────────────────────────────────────────────────────────────────────╮')
        print(line1)
        print(line2)
        print('╰────────────────────────────────────────────────────────────────────────────────────╯\n'+Style.RESET_ALL)


        # print('─'*86)

    except:
        pass