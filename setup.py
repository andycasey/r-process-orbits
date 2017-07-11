from setuptools import setup, find_packages
from codecs import open
from os import path
from re import compile


def read(filename):
    with open(filename, encoding="utf-8") as fp:
        contents = fp.read()
    return contents

here = path.abspath(path.dirname(__file__))

# Get a long description from README.md
long_description = read(path.join(here, "README.md"))

# Get the version information.
vre = compile("__version__ = \"(.*?)\"")
version = vre.findall(read(path.join(here, "code", "__init__.py")))[0]

setup(
    name="gaia-sprint-2017",
    version=version,
    description="Gaia Sprint 2017",
    long_description=long_description,
    url="http://github.com/andycasey/gaia-sprint-2017",
    author="Andrew R. Casey",
    author_email="andrew.casey@monash.edu",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=[],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={}
)