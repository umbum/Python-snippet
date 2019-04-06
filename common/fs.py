"""
    ――――――――――――――――――――――――――――――――――――――――――――――――
    Function              preserves     supports          accepts     copies other
                          permissions   directory dest.   file obj    metadata
    ――――――――――――――――――――――――――――――――――――――――――――――――
    shutil.copy              ✔             ✔                 ☐           ☐
    shutil.copy2             ✔             ✔                 ☐           ✔
    shutil.copyfile          ☐             ☐                 ☐           ☐
    shutil.copyfileobj       ☐             ☐                 ✔           ☐
    ――――――――――――――――――――――――――――――――――――――――――――――――
- windows copy
- xcopy
- forecopy
- etc.
"""

import os
import stat
import shutil
from .log import logger

__all__ = []
# __all__ = ["copyWithoutMeta",
#            "copyWithMeta",
#            "copydir",
#            "rmfile",
#            "rmdir"]



def copyWithoutMeta(src: str, dst: str):
    """shutil.copyfile(src, dst) wrapper
    If dst already exists, raise FileExistsError
    Copy the contents (no metadata) of the file named src to a file named dst and return dst.
    
    Args:
        src (str): src file name
        dst (str): dst file name

    Returns:
        str: dst file name

    Raises:
        FileExistsError: if dst already exist
        IOError: if dst location is not writable
        SameFileError: if src == dst
        FileNotFoundError: if src file not founded
        PermissionError
    """
    logger.info("copyWithoutMeta > {} -> {}".format(src, dst))
    if os.path.exists(dst):
        raise FileExistsError
    return shutil.copyfile(src, dst)


def copyWithMeta(src, dst):
    """shutil.copy2(src, dst) wrapper
    If dst already exists, raise FileExistsError
    copy2() attempts to preserve all file metadata.
    However, It does not guarantee that all file metadata can be copied.
    
    Args:
        src (str): src file name
        dst (str): dst file name

    Returns:
        str: dst file name

    Raises:
        FileExistsError: if dst already exist
        IOError: if dst location is not writable
        SameFileError: if src == dst
        FileNotFoundError: if src file not founded
        PermissionError
    """
    logger.info("copyWithMeta > {} -> {}".format(src, dst))
    if os.path.exists(dst):
        raise FileExistsError("{} already exists.".format(dst))
    return shutil.copy2(src, dst)


def copydir(src, dst):
    """shutil.copytree(src, dst) wrapper

    Args:
        src (str): src file name
        dst (str): dst file name
    """
    logger.info("copydir > {} -> {}".format(src, dst))
    if os.path.exists(dst):
        raise FileExistsError("{} already exists.".format(dst))
    return shutil.copytree(src, dst)

def rmfile(path):
    """os.remove(path) wrapper

    Args:
        path (str || bytes || directory descriptor)

    Raises:
        OSError: If path is directory.
        FileNotFoundError
    """
    logger.info("rmfile > {}".format(path))
    try:
        os.remove(path)
    except PermissionError as e:
        _rmHandler(os.remove, path, None)

def rmdir(path):
    """shutil.rmtree(path, onerror=_rmHandler) wrapper

    Args:
        path (str || bytes || directory descriptor)
    """
    logger.info("rmdir > {}".format(path))
    shutil.rmtree(path, onerror=_rmHandler)

def _rmHandler(_remove, path, _):
    logger.debug("rmHandler : Clear the readonly bit and reattempt > {}".format(path))
    os.chmod(path, stat.S_IWRITE)
    _remove(path)


if __name__ == "__main__":
    # rmdir("asdf")
    # rmfile("a.bmp")
    copydir("../T1002_Data_Compressed", "cdir")

