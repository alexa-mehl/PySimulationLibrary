from distutils.core import setup
"""
from distutils.command.install import INSTALL_SCHEMES

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib'] + "/PySimLib"
"""
setup(
    # Application name:
    name="PySimLib",

    # Version number (initial):
    version="1.0",

    # Application author details:
    author="Alexandra Mehlhase",
    author_email="a.mehlhase@tu-berlin.de",
    
    description="Python Simulation Library",

    # Packages
    packages=["PySimLib", "PySimLib.Exceptions", "PySimLib.Mat", "PySimLib.Models", "PySimLib.Solvers", "PySimLib.Tools"],
)
