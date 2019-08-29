# coding: utf-8

import os
from setuptools import setup, find_packages
import importlib
import re

# Vars to set:
description = "This project gathers some useful basics Python functions and class."
author = "hayj"
author_email = "hj@hayj.fr"
version = "0.0.92" # replaced by the version in the main init file if exists

# Current dir:
thelibFolder = os.path.dirname(os.path.realpath(__file__))

# We take all requirements from the file or you can set it here :
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Example : ["gunicorn", "docutils >= 0.3", "lxml==0.5a7"]
dependency_links = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        dependency_links = []
        install_requires = []
        required = f.read().splitlines()
        for current in required:
            if 'git' in current:
                if "https" not in current:
                    current = current.replace("-e git", "https")
                    current = current.replace(".git#egg", "/zipball/master#egg")
                dependency_links.append(current)
            else:
                install_requires.append(current)

# dependency_links is deprecated, see https://serverfault.com/questions/608192/pip-install-seems-to-be-ignoring-dependency-links
dependency_links = []

# We search a folder containing "__init__.py":
def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]
mainPackageName = thelibFolder.lower().split('/')[-1]
for dirname, dirnames, filenames in walklevel(thelibFolder):
    if "__init__.py" in filenames:
        mainPackageName = dirname.split("/")[-1]
packagePath = thelibFolder + '/' + mainPackageName
# Get the version of the lib in the __init__.py:
initFilePath = packagePath + '/' + "__init__.py"
if os.path.isdir(packagePath):
    with open(initFilePath, 'r') as f:
        text = f.read()
        result = re.search('^__version__\s*=\s*["\'](.*)["\']', text, flags=re.MULTILINE)
        if result is not None:
            version = result.group(1)

# To import the lib, use:
# thelib = importlib.import_module(mainPackageName)

# Readme content:
readme = None
readmePath = thelibFolder + '/README.md'
if os.path.isfile(readmePath):
    try:
        print("Trying to convert README.md to rst format...")
        import pypandoc
        readme = pypandoc.convert(readmePath, 'rst')
    except(IOError, ImportError) as e:
        print(e)
        print("Cannot use pypandoc to convert the README...")
        readme = open(readmePath).read()
else:
    print("README.md not found.")


# The whole setup:
setup(

    # The name for PyPi:
    name="systools", # systemtools, hjsystemtools

    # The version of the code which is located in the main __init__.py:
    version=version,

    # All packages to add:
    packages=find_packages(),

    # About the author:
    author=author,
    author_email=author_email,

    # A short desc:
    description=description,

    # A long desc with the readme:
    long_description=readme,

    # Dependencies:
    install_requires=install_requires,
    dependency_links=dependency_links,
    
    # For handle the MANIFEST.in:
    include_package_data=True,

    # The url to the official repo:
    # url='https://',

    # You can choose what you want here : https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ],

    # If you want a command line like "do-something", on a specific funct of the package :
#     entry_points = {
#         'console_scripts': [
#             'wm-setup = workspacemanager.setup:generateSetup',
#             'wm-pew = workspacemanager.venv:generateVenv',
#             'wm-deps = workspacemanager.deps:installDeps',
#         ],
#     },
)







