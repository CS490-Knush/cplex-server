# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "cplex_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Cplex Server",
    author_email="apiteam@swagger.io",
    url="",
    keywords=["Swagger", "Cplex Server"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['cplex_server=cplex_server.__main__:main']},
    long_description="""\
    This is the API that will run on the cplex server. Scheduling agents can call this API.  You can find  out more about Swagger at  [http://swagger.io](http://swagger.io) or on  [irc.freenode.net, #swagger](http://swagger.io/irc/). 
    """
)

