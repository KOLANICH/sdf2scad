mol2scad.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
[![PyPi Status](https://img.shields.io/pypi/v/mol2scad.svg)](https://pypi.python.org/pypi/mol2scad)
[![GitLab Build Status](https://gitlab.com/KOLANICH/mol2scad.py/badges/master/pipeline.svg)](https://gitlab.com/KOLANICH/mol2scad.py/pipelines/master/latest)
![GitLab Coverage](https://gitlab.com/KOLANICH/mol2scad.py/badges/master/coverage.svg)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/mol2scad.py.svg)](https://coveralls.io/r/KOLANICH/mol2scad.py)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/mol2scad.py.svg)](https://libraries.io/github/KOLANICH/mol2scad.py)

This tool converts `mol` and `sdf` files into OpenSCAD files showing a 3D model of a molecule. Either run it in this folder or copy `util.scad` to the folder with generated files. Also you will need [scad-utils](https://github.com/OskarLinde/scad-utils.git) either installed or put in the same dir.

Requirements
------------
* [`mollusk`](https://github.com/georglind/mollusk) [![TravisCI Build Status](https://travis-ci.org/georglind/mollusk.svg?branch=master)](https://travis-ci.org/georglind/mollusk) ![License](https://img.shields.io/github/license/georglind/mollusk.svg) - `mol` (and `sdf`) file parser
* [`webcolors`](https://github.com/ubernostrum/webcolors) [![PyPi Status](https://img.shields.io/pypi/v/webcolors.svg)](https://pypi.python.org/pypi/webcolors) [![TravisCI Build Status](https://travis-ci.org/ubernostrum/webcolors.svg?branch=master)](https://travis-ci.org/ubernostrum/webcolors) ![License](https://img.shields.io/github/license/ubernostrum/webcolors.svg) - colors
* [SolidPython](https://github.com/SolidCode/SolidPython) [![PyPi Status](https://img.shields.io/pypi/v/plumbum.svg)](https://pypi.python.org/pypi/solid) [![TravisCI Build Status](https://travis-ci.org/SolidCode/SolidPython.svg?branch=master)](https://travis-ci.org/SolidCode/SolidPython) ![License](https://img.shields.io/github/license/SolidCode/SolidPython.svg) - OpenSCAD AST
* `mendeleev` [![PyPi Status](https://img.shields.io/pypi/v/mendeleev.svg)](https://pypi.org/pypi/mendeleev) - chemical elements database
* [`plumbum`](https://github.com/tomerfiliba/plumbum) [![PyPi Status](https://img.shields.io/pypi/v/plumbum.svg)](https://pypi.org/pypi/plumbum)
  [![TravisCI Build Status](https://travis-ci.org/tomerfiliba/plumbum.svg?branch=master)](https://travis-ci.org/tomerfiliba/plumbum)
 ![License](https://img.shields.io/github/license/tomerfiliba/plumbum.svg) - for command line interface
