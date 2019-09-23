"""Setup the package."""

from setuptools import find_packages, setup

setup(
    name="shlack",
    version="0.1",
    packages=["shlack"],
    install_requires=[],
    extras_require={"dev": ["pytest", "black", "pydocstyle"]},
)
