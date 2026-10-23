
import os
from pathlib import Path
import json


def _user_config_path() -> Path:
    ''' Path where config JSON is stored'''
    env = os.environ.get("MIDAS_CIVIL_CONFIG")
    if env:
        return Path(env).expanduser()
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        
    return base / "midas_civil_python" / "config.json"


def _generate_configJSON():
    '''Generates and returns the JSON data'''
    from ._mapi import NX
    _CONFIG_JSON = {}
    _CONFIG_JSON["SHOW_OUPTUT_IN_TERMINAL"] = NX.SHOW_OUPTUT_IN_TERMINAL
    _CONFIG_JSON["SAVE_DEBUG_LOG"] = NX.SAVE_DEBUG_LOG
    _CONFIG_JSON["SEND_IN_CHUNKS"] = NX.SEND_IN_CHUNKS
    _CONFIG_JSON["SYS_EXIT_ON_ERROR"] = NX.SYS_EXIT_ON_ERROR
    _CONFIG_JSON["debug_request"] = NX.debug_request
    _CONFIG_JSON["dispWarning"] = NX.dispWarning
    _CONFIG_JSON["OFFLINE"] = NX.OFFLINE

    return _CONFIG_JSON

    
# SAVE THE JSON FILE
def _save_config_file(data):
    '''Generates current config data and saves'''
    import tempfile
    p = _user_config_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=".config-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(tmp, p)          # atomic: no half-written file on crash
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
    if os.name != "nt":
        try:
            os.chmod(p, 0o600)      # file holds the MAPI key -> owner-only
        except OSError:
            pass
    return p


# LOAD THE CONFIG IN CIVIL LIB
def _load_config_inLIB():
    path = _user_config_path()
    if not path.is_file():
        _CONFIG_JSON =  _generate_configJSON()
        _save_config_file(_CONFIG_JSON)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _CONFIG_JSON =  data
    except Exception as e:
        _CONFIG_JSON =  _generate_configJSON()

    from ._mapi import NX
    NX.SHOW_OUPTUT_IN_TERMINAL = _CONFIG_JSON["SHOW_OUPTUT_IN_TERMINAL"]
    NX.SAVE_DEBUG_LOG = _CONFIG_JSON["SAVE_DEBUG_LOG"]
    NX.SEND_IN_CHUNKS = _CONFIG_JSON["SEND_IN_CHUNKS"]
    NX.OFFLINE = _CONFIG_JSON["OFFLINE"]
    NX.SYS_EXIT_ON_ERROR = _CONFIG_JSON["SYS_EXIT_ON_ERROR"]
    NX.debug_request = _CONFIG_JSON["debug_request"]
    NX.dispWarning = _CONFIG_JSON["dispWarning"]

from typing import Literal
_configField = Literal["SAVE_DEBUG_LOG","debug_request","OFFLINE","SEND_IN_CHUNKS","SYS_EXIT_ON_ERROR","SHOW_OUPTUT_IN_TERMINAL","dispWarning"]


def MIDAS_Configure(data:_configField,value):

    path = _user_config_path()

    with open(path, "r", encoding="utf-8") as f:
        js_config = json.load(f)
    _CONFIG_JSON =  js_config

    _CONFIG_JSON[data] = value
    
    _save_config_file(_CONFIG_JSON)