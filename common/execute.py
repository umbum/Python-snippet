import sys
import subprocess
import json
from .log import logger

__all__ = ["run"]

def run(args, *, stdout=subprocess.PIPE, universal_newlines=True, **kwargs):
    """subprocess.run(args, **kwargs) wrapper

    Args:
        args (iterable):
        **kwargs (key=value): keyword arguments

    Example:
        >>> import common
        >>> result = common.run(["ls", "-a"], stderr=2)  # or "ls -a"
        >>> print(result)
        >>> print(result.stdout)
    """
    logger.info(str(args) + json.dumps(kwargs))
    return subprocess.run(args, stdout=stdout, universal_newlines=universal_newlines, **kwargs)



if __name__ == "__main__":
    print(run("echo asdf").stdout)
    print(run(["echo", "asdf"]).stdout)