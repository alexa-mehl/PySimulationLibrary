"""
  Copyright (C) 2014-2018  Alexandra Mehlhase <a.mehlhase@tu-berlin.de>, All Rights Reserved
  
  Implemented by Alexandra Mehlhase, Amir Czwink
  
  This file is part of the AMSUN project
  (https://gitlab.tubit.tu-berlin.de/groups/amsun)

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
   
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages;

setup(
    name="PySimLib",
    version="1.0.0b7",
    description="The Python Simulation Library allows to simulate Modelica and Simulink models in a platform-independent way.",
    url = "https://gitlab.tubit.tu-berlin.de/a.mehlhase/PySimulationLibrary",
    author="Alexandra Mehlhase",
    author_email="a.mehlhase@tu-berlin.de",
    packages = ["PySimLib", "PySimLib.Exceptions", "PySimLib.Mat", "PySimLib.Models", "PySimLib.Solvers", "PySimLib.Tools"],
    license = "GPL",
    
    install_requires = [
        "matplotlib",
        "pymatbridge" #needs "zmq"
    ],
)

"""
versioning:
	1.0.0.dev1 development release
	1.0.0.a1 alpha release
	1.0.0.b1 beta release
	1.0.0.rc1 release candidate
	1.0.0 final release
"""
