from winreg import *
from .log import logger

__all__ = []
# __all__ = ["create", "delete"]

def _resolveHiveStr(hive_str: str):
    if hive_str in ("HKEY_CLASSES_ROOT", "HKCR"):
        hive = HKEY_CLASSES_ROOT
    elif hive_str in ("HKEY_CURRENT_USER", "HKCU"):
        hive = HKEY_CURRENT_USER
    elif hive_str in ("HKEY_LOCAL_MACHINE", "HKLM"):
        hive = HKEY_LOCAL_MACHINE
    elif hive_str in ("HKEY_USERS", "HKU"):
        hive = HKEY_USERS
    elif hive_str in ("HKEY_CURRENT_CONFIG", "HKCC"):
        hive = HKEY_CURRENT_CONFIG
    elif hive_str in ("HKEY_DYN_DATA", "HKDD"):
        hive = HKEY_DYN_DATA
    elif hive_str in ("HKEY_PERFORMANCE_DATA", "HKPD"):
        hive = HKEY_PERFORMANCE_DATA
    else:
        # logger.error("hive_str is unknown string : ({})".format(hive_str))
        raise ValueError("hive_str is unknown string : ({})".format(hive_str))
    return hive

def _resolveValueType(type_str: str):
    if type_str == "REG_SZ":
        reg_type = REG_SZ
    elif type_str == "REG_BINARY":
        reg_type = REG_BINARY
    elif type_str == "REG_DWORD":
        reg_type = REG_DWORD
    return reg_type

def _splitHive(path: str):
    split = path.index("\\")
    hive_str, sub_key = path[:split], path[split+1:]
    hive = _resolveHiveStr(hive_str)
    return hive, sub_key


def create(path: str, value_name=None, data=None, type_str="REG_SZ"):
    """
    :param path: (str)
    :param value_name: (str, default=None)
    :param data: (depends on type_str, default=None)
    :param type_str: (str) REG_SZ(default), REG_DWORD, REG_BINARY
    :return: key path

    Example:
        >>> k0 = create("HKEY_CURRENT_USER\\Software\\Classes\\ms-settings")
        >>> k1 = create("HKEY_CURRENT_USER/Software/Classes/ms-settings", "TestValue1", "test string")
        >>> k2 = create("HKEY_CURRENT_USER\\Software/Classes\\ms-settings", "TestValue2", 2, "REG_DWORD")
    """
    path = path.replace("/", "\\")
    hive, sub_key = _splitHive(path)

    key = CreateKey(hive, sub_key)
    reg_type = _resolveValueType(type_str)
    SetValueEx(key, value_name, 0 , reg_type, data)
    CloseKey(key)
    logger.info("Registry created > {} ({}={}) type:{}".format(path, value_name, data, type_str))
    return path


def delete(path: str, value=None):
    """
    Args:
        path  (str): key path string
        value (str, default=None): value string

    Example:
        >>> path = "HKEY_CURRENT_USER\\Software\\Classes\\ms-settings"
        >>> # delete key and its all values.
        >>> delete(path)
        >>> 
        >>> # delete specific value.
        >>> delete(path, "DelegateExecute")
    """
    path = path
    path = path.replace("/", "\\")
    hive, sub_key = _splitHive(path)
    if value is not None:
        with OpenKey(hive, sub_key, access=KEY_WRITE) as key:
            DeleteValue(key, value)
        logger.info("Registry deleted > {} {}".format(path, value))
    else:
        DeleteKey(hive, sub_key)
        logger.info("Registry deleted > {}".format(path))



if __name__ == "__main__":
    ### test
    key_path = create("HKEY_CURRENT_USER\\Software\\Classes\\ms-settings")
    key_path1 = create("HKEY_CURRENT_USER/Software/Classes/ms-settings", "TestValue1", "test string")
    key_path2 = create("HKEY_CURRENT_USER\\Software/Classes\\ms-settings", "TestValue2", 2, "REG_DWORD")
    key_path3 = create("HKEY_CURRENT_USER\\Software/Classes\\ms-settings", "TestValue3", "test string3")

    delete(key_path3, "TestValue2")
    delete("HKEY_CURRENT_USER\\Software/Classes\\ms-settings", "TestValue3")

    # import time
    # time.sleep(5)
    delete("HKEY_CURRENT_USER\\Software/Classes\\ms-settings")


