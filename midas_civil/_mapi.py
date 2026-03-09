import requests
import sys
from colorama import Fore, Style
try:import winreg
except: pass
import time
from tqdm import tqdm
# import polars as pl



def Midas_help():
    """MIDAS Documnetation : https://midas-rnd.github.io/midasapi-python """
    print('\n╭────────────────────────────────────────────────────────────────────────────────────╮')
    print("│         HELP MANUAL   :     https://midas-rnd.github.io/midasapi-python/           │")
    print('╰────────────────────────────────────────────────────────────────────────────────────╯\n')



class NX:
    version_check = True    # CHANGE IT TO FALSE TO SKIP VERSION CHECK OF LIBRARY
    user_print = True
    debug_request = False
    debug_requestJSON = False
    debug_response = False
    onlyNode = False
    visualiser = False
    modelIDs = {} # Handles the fast MAX ID
    autoTaperGroup = False

    # Function for quick saving of JSON
    @staticmethod
    def saveJSON(jsonData,fileLocation = "jsData.json"):
        import json
        with open(fileLocation, "w", encoding="utf-8") as f:
            json.dump(jsonData, f, indent=4, ensure_ascii=False)
        return True

    # Function to quickly print text in a box , width -> CENTER Align
    @staticmethod
    def box_print(text:str="HELLO WORLD",width:int=82,pad:int=1,text_col=Fore.WHITE,border_col=Fore.LIGHTWHITE_EX):
        col_border = border_col
        col_text = text_col

        padding = pad

        lines = text.splitlines()

        length = max([len(line) for line in lines])

        if width:
            length = max(length,width)
        leng = length+2*padding


        print(col_border+"╭","─"*leng,"╮",sep="")
        for line in lines:
            if width:
                gap = (leng-len(line))//2
                print("│"," "*gap,col_text+line," "*(leng-len(line)-gap),col_border+"│",sep="")
            else:
                print("│"," "*padding,col_text+line," "*(leng-padding-len(line)),col_border+"│",sep="")
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

            tqdm.write(f' 🌐   BASE URL is taken from Registry entry.  >>  {url_comb}')
            MAPI_BASEURL(url_comb)
        except:
            tqdm.write(" 🌐   BASE URL is not defined. Click on Apps > API Settings to copy the BASE URL Key.\nDefine it using MAPI_BASEURL('https://moa-engineers.midasit.com:443/civil')")
            sys.exit(0)

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
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                MAPI_BASEURL(base_url)
                MAPI_BASEURL.server_loc = serv_locations[i]
                chk=1
                break
        if chk==0:
            tqdm.write(f" 🌐   Kindly manually enter the BASE URL. \nRefer to https://moa.midasit.com/services to find the correct URL.")
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
                tqdm.write(f' 🔑   MAPI-KEY is taken from Registry entry.  >>  {my_key[:35]}...')
            except:
                tqdm.write(f"🔑   MAPI KEY is not defined. Click on Apps > API Settings to copy the MAPI Key.\n Define it using MAPI_KEY('xxxx')")
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
        tqdm.write(Fore.RED+f">>   METHOD : {method} |  URL : {command} | STATUS :  {response.status_code} | TIME : {elapsed_time:.4f} sec "+Style.RESET_ALL)
    if NX.debug_requestJSON:
        tqdm.write(Fore.CYAN+">>  "+str(body)+Style.RESET_ALL)
    if NX.debug_response:
        tqdm.write(Fore.GREEN+"<<  "+str(response.json())+Style.RESET_ALL)

    if MAPI_KEY.count == 0:
        MAPI_KEY.count = -1
        if response.status_code == 404:
            print(Fore.RED +'\n╭─ 💀   ─────────────────────────────────────────────────────────────────────────────╮')
            print(f"│  Civil NX model is not connected.  Click on 'Apps > Connect' in Civil NX.          │")
            print(f"│  Make sure the MAPI Key in python code is matching with the MAPI key in Civil NX.  │")
            print('╰────────────────────────────────────────────────────────────────────────────────────╯\n'+Style.RESET_ALL)
            sys.exit(0)
        elif response.status_code == 401:
            print(Fore.RED +'\n╭─ 💀   ─────────────────────────────────────────────────────────────────────────────╮')
            print(f"│  MAPI KEY entered is invalid.                                                      │")
            print(f"│  Please consider refreshing MAPI-Key in CIVIL NX and resending the request.        │")
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
    response =  MidasAPI('GET','/config/ver',{})
    if 'VER' in response:
        resp = response['VER']

        # print(f"{' '*15}Connected to {resp['NAME']}")
        # print(f"{' '*15}USER : {resp['USER']}          COMPANY : {resp['COMPANY']}")

        ln1 = f"Connected to {resp['NAME']}            SERVER : {MAPI_BASEURL.server_loc}"
        ln2 = f"USER : {resp['USER']}          COMPANY : {resp['COMPANY']}"

        lg_ln1 = 66-len(ln1)
        lg_ln2 = 70-len(ln2)

        line1 = f"│{' '*12} {ln1} {' '*lg_ln1} 🟢 │"
        line2 = f"│{' '*12} {ln2} {' '*lg_ln2}│"
        tqdm.write(Fore.GREEN+'\n╭─ 🔔  ──────────────────────────────────────────────────────────────────────────────╮')
        tqdm.write(line1)
        tqdm.write(line2)
        tqdm.write('╰────────────────────────────────────────────────────────────────────────────────────╯\n'+Style.RESET_ALL)


        # print('─'*86)

