import requests
import sys
import winreg


def Midas_help():
    """MIDAS Documnetation : https://midas-rnd.github.io/midasapi-python """
    print("---"*22)
    print("|   HELP MANUAL : https://midas-rnd.github.io/midasapi-python/   |")
    print("---"*22,"\n")



class MAPI_PRODUCT:
    product = "civil"

    def __init__(self,product:str):
        """Product 'civil' or 'gen'"""
        if product.lower() == 'gen':
            MAPI_PRODUCT.product = 'gen'


class MAPI_KEY:
    """MAPI key from Civil NX.\n\nEg: MAPI_Key("eadsfjaks568wqehhf.ajkgj345")"""
    data = ""
    
    def __init__(self, mapi_key:str):
        MAPI_KEY.data = mapi_key
        
    @classmethod
    def get_key(cls):
        if MAPI_KEY.data == "":
            try:
                key_path = r"Software\\MIDAS\\CVLwNX_US\\CONNECTION"  
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                value = winreg.QueryValueEx(registry_key, "Key")
                my_key = value[0]
                print(' 🔑  MAPI KEY is not defined. MAPI-KEY is taken from Registry entry.')
                MAPI_KEY(my_key)
            except:
                print(f"🔑   MAPI KEY is not defined. Click on Apps > API Settings to copy the MAPI Key.")
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
    
    base_url = f"https://moa-engineers.midasit.com:443/{MAPI_PRODUCT.product}"
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


