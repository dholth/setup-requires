#!/usr/bin/env python
# Install dependencies listed in pyproject.toml, then
# continue with regularly scheduled setup.py.
# From https://bitbucket.org/dholth/setup-requires

import sys, subprocess, pkg_resources

sys.path[0:0] = ['setup-requires']
pkg_resources.working_set.add_entry('setup-requires')

def missing_requirements(specifiers):
    for specifier in specifiers:
        try:
            pkg_resources.require(specifier)
        except pkg_resources.DistributionNotFound:
            yield specifier

def install_requirements(specifiers):
    to_install = list(specifiers)
    if to_install:
        subprocess.call([sys.executable, "-m", "pip", "install", 
            "-t", "setup-requires"] + to_install)
        
install_requirements(missing_requirements(['toml']))

import toml

try:
    pyproject = toml.load('pyproject.toml')
except IOError:
    pass
else:
    requires = pyproject.get('build-system', {}).get('requires')
    install_requirements(missing_requirements(requires))

### Place normal setup.py contents below ###

from setuptools import setup

setup(name="example-package",
    version = "0.0.1",
    py_modules = [ 'example_package' ],
    install_requires = [ ],
    description = "An example of a package with setup requirements.",
    license = "MIT",
    author = "Emilio Example",
    author_email = "emilio@example.org",
    url="https://bitbucket.org/dholth/setup-requires")

# Alternatively, run real-setup.py from a separate file
# exec(compile(open("real-setup.py").read().replace('\\r\\n', '\\n'),
#     __file__,
#     'exec'))
