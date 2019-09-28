"""Setup the package."""

from setuptools import find_packages, setup

setup(
    name="shlack",
    version="0.1",
    packages=["shlack", "shlack.cli"],
    install_requires=["slacker", "click"],
    extras_require={"dev": ["pytest", "black", "pydocstyle"]},
    entry_points={"console_scripts": ["shlack = shlack.cli.__main__:cli"]},
)
