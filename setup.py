#!/usr/bin/env python3

import setuptools
from pathlib import Path

readme = Path("README.md").read_text()

setuptools.setup(
    name="ligeia",
    packages=["ligeia"],
    version="0.1",
    license="GPL3",
    description="Python3 Package for voice synthesis using "
            "eSpeak and PicoTTS.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Carlos A. Planchón",
    author_email="bubbledoloresuruguay2@gmail.com",
    url="https://github.com/carlosplanchon/ligeia",
    download_url="https://github.com/carlosplanchon/"
        "ligeia/archive/v0.1.tar.gz",
    keywords=["Ligeia", "voice", "synthesis", "eSpeak", "PicoTTS"],
    install_requires=[
        "playsound",
        "servussymtowords",
        "sudoaptinstall",
        "tokenizesentences"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
