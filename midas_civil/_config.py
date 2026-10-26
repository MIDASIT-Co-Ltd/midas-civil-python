
import os
from pathlib import Path
import json
from typing import Literal

# Options stored in the config file (all booleans)
_CONFIG_KEYS = ("SHOW_OUPTUT_IN_TERMINAL","SAVE_DEBUG_LOG","SEND_IN_CHUNKS","SYS_EXIT_ON_ERROR","debug_request","dispWarning","OFFLINE")
_configField = Literal["SAVE_DEBUG_LOG","debug_request","OFFLINE","SEND_IN_CHUNKS","SYS_EXIT_ON_ERROR","SHOW_OUPTUT_IN_TERMINAL","dispWarning"]


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
    '''Generates and returns the JSON data from the current NX options'''
    from ._mapi import NX
    return {key: getattr(NX, key) for key in _CONFIG_KEYS}


# SAVE THE JSON FILE
def _save_config_file(data):
    '''Saves the config data (atomic write)'''
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
            os.chmod(p, 0o600)      # owner-only (the file holds options only, never the MAPI key)
        except OSError:
            pass
    return p


def _read_config_file() -> dict:
    '''Returns the stored config dict, or {} when the file is missing or unreadable.'''
    path = _user_config_path()
    try:
        if path.is_file():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


# LOAD THE CONFIG IN CIVIL LIB
def _load_config_inLIB():
    '''Applies the stored options to NX. Missing / invalid keys keep their defaults, so an
    older or hand-edited file never breaks the import. A read-only location is ignored.'''
    from ._mapi import NX
    data = _read_config_file()

    for key in _CONFIG_KEYS:
        value = data.get(key)
        if isinstance(value, bool):
            setattr(NX, key, value)

    # Complete the file with any missing key (keeps unknown keys untouched)
    if any(not isinstance(data.get(key), bool) for key in _CONFIG_KEYS):
        try:
            _save_config_file({**data, **_generate_configJSON()})
        except OSError:
            pass


def MIDAS_Configure(data:_configField,value:bool):
    '''Saves an option in the config file (used by every future session) and applies it to the current session.

    MIDAS_Configure("SHOW_OUPTUT_IN_TERMINAL", False)
    MIDAS_Configure("SYS_EXIT_ON_ERROR", False)
    '''
    if data not in _CONFIG_KEYS:
        raise ValueError(f"Unknown config option {data!r}. Valid options are: {', '.join(_CONFIG_KEYS)}")
    if not isinstance(value, bool):
        raise ValueError(f"Config option {data!r} must be True or False, got {value!r}")

    from ._mapi import NX
    setattr(NX, data, value)

    _CONFIG_JSON = {**_generate_configJSON(), **_read_config_file()}
    _CONFIG_JSON[data] = value
    _save_config_file(_CONFIG_JSON)
