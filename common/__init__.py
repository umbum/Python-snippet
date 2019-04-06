"""
Usage
-----
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import common
"""
import os
from .log import logger
from .fs import *
from .execute import run
from .reg import *

__author__  = "umbum <umbum7601@gmail.com>"

__all__ = (fs.__all__ +
           log.__all__ +
           execute.__all__ +
           reg.__all__)


BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

