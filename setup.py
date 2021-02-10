#    Copyright 2021 Jalaj Kumar
#    This file is part of cly.

#    cly is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    cly is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.

#    You should have received a copy of the GNU Lesser General Public License
#    along with cly.  If not, see <https://www.gnu.org/licenses/>

from setuptools import setup, find_packages


def read_file(fname: str) -> str:
    f = open(fname, "r")
    txt = f.read()
    f.close()
    return txt


setup(
    name="cly",
    version="0.1.0.dev1",
    description="An amazing tool to make powerful and robust command line interfaces",
    long_description=read_file("./README.md"),
    long_description_conotent_type="text/markdown",
    url="",  # TODO
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
    keywords="cli commands development terminal",
    packages=find_packages(),
    license="LGPLv3",
    python_requires=">=3.6",
)
