"""Tests for the config reader module."""

import time

from shlack.runner import detachify


def test_detachify(tmp_path):
    """Test that deatchification does not result in an error.
    
    I don't know how to test os.fork but have verified it has the expected result 
    for the vanilla case. It checks

    - That the process was detached
    - And a known string was written to a file
    """
    now_str = str(round(time.time(), 3))
    tmp_file = tmp_path / "temporary.txt"

    def write_string(s):
        """Write a string to the temp file."""
        time.sleep(0.05)
        with open(tmp_file, "w") as f:
            f.write(s)

    # run it and assert that it took less than the wait time to move on
    # if it took _longer_ than the function might not have been detached.
    t1 = time.time()
    detachify(write_string)(now_str)
    t2 = time.time()
    assert (t2 - t1) < 0.05

    # wait a little and check the file that was written.
    time.sleep(0.15)

    with open(tmp_file, "r") as f:
        assert now_str == f.read()
