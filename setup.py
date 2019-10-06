"""Setup the package."""

import os

from setuptools import find_packages, setup

# use readme as long description
README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "readme.md")

with open(README_PATH) as file_:
    LONG_DESCRIPTION = file_.read()

setup(
    name="shlack",
    version="0.1.1",
    description="Yet another slack command line interface.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Nolan Conaway",
    author_email="nolanbconaway@gmail.com",
    url="https://github.com/nolanbconaway/shlack",
    classifiers=[
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords=["slack", "cli"],
    license="MIT",
    packages=["shlack", "shlack.cli"],
    install_requires=["slacker", "click"],
    entry_points={"console_scripts": ["shlack = shlack.cli.__main__:cli"]},
)
