import requests
import sys
import winreg


def Midas_help():
    """MIDAS Documnetation : https://midas-rnd.github.io/midasapi-python """
    print("---"*22)
    print("|   HELP MANUAL : https://midas-rnd.github.io/midasapi-python/   |")
    print("---"*22,"\n")



class MAPI_COUNTRY:
    
    country = "US"

    def __init__(self,country:str):
        ''' Define Civil NX country to automatically set Base URL and MAPI Key from registry.
        ```
        MAPI_COUNTRY('US') # For english version
        MAPI_COUNTRY('KR') # For Korean version
        MAPI_COUNTRY('CN') # For Chinese version
        ```
        '''
        if country.lower() in ['us','cn','kr','jp']:
            MAPI_COUNTRY.country = country.upper()
        else:
            MAPI_COUNTRY.country = 'US'
        
        MAPI_BASEURL.set_url()
        MAPI_KEY.get_key()


class MAPI_BASEURL:
    baseURL = "https://moa-engineers.midasit.com:443/civil"
    
    def __init__(self, baseURL:str):
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
                print(f' 🔑   MAPI-KEY is taken from Registry entry.  >>  {my_key[:35]}...')
                MAPI_KEY(my_key)
            except:
                print(f"🔑   MAPI KEY is not defined. Click on Apps > API Settings to copy the MAPI Key.\n Define it using MAPI_KEY('xxxx')")
                sys.exit(0)
        else:
            my_key = MAPI_KEY.data
        return my_key
#---------------------------------------------------------------------------------------------------------------

#2 midas API link code:
def MidasAPI(method:str, command:str, body:dict={})->dict:
    f"""Sends HTTP Request to MIDAS Civil NX
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

    if method == "POST":
        response = requests.post(url=url, headers=headers, json=body)
    elif method == "PUT":
        response = requests.put(url=url, headers=headers, json=body)
    elif method == "GET":
        response = requests.get(url=url, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url=url, headers=headers)

    if response.status_code == 404: 
        print(f"⚠️  Civil NX model is not connected.  Click on 'Apps> Connect' in Civil NX. \nMake sure the MAPI Key in python code is matching with the MAPI key in Civil NX.\n\n")
        sys.exit(0)

    # print(method, command, response.status_code , "✅")

    return response.json()


