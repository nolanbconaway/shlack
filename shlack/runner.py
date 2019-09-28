"""Utilities for launching processes in background tasks."""
import os
import subprocess
from multiprocessing import Process


def detachify(func):
    """Decorate a function so that its calls are async in a detached process.
    
    Usage
    -----

    .. code::
        import time

        @detachify
        def f(message):
            time.sleep(5)
            print(message)

        f('Async and detached!!!')

    """
    # create a process fork and run the function
    def forkify(*args, **kwargs):
        pid = os.fork()
        if pid != 0:
            return pid
        func(*args, **kwargs)

    # wrapper to run the forkified function
    def wrapper(*args, **kwargs):
        proc = Process(target=lambda: forkify(*args, **kwargs))
        proc.start()
        proc.join()
        return

    return wrapper


def shell_command(command_str):
    """Run a shell command as a string, returning a tuple of (stdout, stderr)."""
    try:
        out = subprocess.check_output(command_str, shell=True, stderr=subprocess.STDOUT)
        if out is not None:
            out = out.decode()
        err = None
    except subprocess.CalledProcessError as e:
        err = e.output.decode()
        out = None

    return out, err
