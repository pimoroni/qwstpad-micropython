# Boilerplate MicroPython

This boilerplate repository is intended to be a starting point for library
authors creating a `mip`-compatible library that is also available via
PyPI (and thus installable by Thonny's Tools -> Manage Packages.)

## package.json

Specify a package installable via `mip`.

The format for this file is documented at https://docs.micropython.org/en/latest/reference/packages.html#writing-publishing-packages

You can generate it automatically by running `make package.json`, though
this will not handle dependencies.

## pyproject.toml

Specify a Python package which can be built with `hatch` and deployed to
the Python Package Index.