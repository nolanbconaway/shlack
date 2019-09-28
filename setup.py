"""Setup the package."""

from setuptools import find_packages, setup

setup(
    name="shlack",
    version="0.1",
    packages=["shlack", "shlack.cli"],
    install_requires=["slacker==0.13.0", "click==7.0"],
    extras_require={"dev": ["pytest==5.1.3", "black==19.3b0", "pydocstyle==4.0.1"]},
    entry_points={"console_scripts": ["shlack = shlack.cli.__main__:cli"]},
)
