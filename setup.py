# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

setup (
    name = "subset",
    version = "1.0.dev",

    entry_points = {
        "console_scripts": [
            "subset = subset:main",
        ]
    },

    install_requires = [
        "ply"
    ],

    author = "erning"
)