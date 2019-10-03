"""Setup the package."""

from setuptools import find_packages, setup

setup(
    name="shlack",
    version="0.1.1",
    packages=["shlack", "shlack.cli"],
    install_requires=["slacker", "click"],
    entry_points={"console_scripts": ["shlack = shlack.cli.__main__:cli"]},
)
