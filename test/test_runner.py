"""Tests for the runner module."""
import os
import time

from shlack.runner import detachify, shell_command


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


def test_detachify_env_persist(monkeypatch, tmp_path):
    """Test that the user env is used in the deatched process."""
    tmp_file = tmp_path / "temporary.txt"
    now_str = str(round(time.time(), 3))
    monkeypatch.setenv("ENV_VARIABLE", now_str)

    def f():
        os.system("echo $ENV_VARIABLE > %s" % tmp_file)

    detachify(f)()
    time.sleep(0.05)

    with open(tmp_file, "r") as f:
        assert now_str == f.read().strip()


def test_shell_good_command():
    """Test that shell command works when the command is known to work."""
    out, err = shell_command("ls .")
    assert err is None
    assert "test" in out


def test_shell_bad_command():
    """Test that shell command works when the command is known to work."""
    out, err = shell_command("ls adasdasdas")
    assert out is None
    assert "adasdasdas" in err
