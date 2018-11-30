import os
from setuptools import setup, find_packages
import json

# read the file containing the package requirements in pip
# and use it also for the package requirements here
with open('./config/requirements.txt') as f:
    content = f.readlines()

# read the version file and convert it to a python dict
with open('./config/version.json') as f:
    cfg_dict = json.load(f)

# name from cofngi file
NAME = cfg_dict['progname']
# version from config file
VERSION = cfg_dict['version']

setup(
    name=NAME,
    version=VERSION,
    description='Library Managament Service (LMS)',
    license='PSF',
    author='Venu Nayar',
    author_email='venu.nayar@github.com',
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Systems Administration',
        'License :: PSF',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
    # find required packages in source excluding venv
    packages=find_packages(where='./', exclude=['venv']),
    # include any extra package data (static files etc)
    include_package_data=True,
    # install packages fromn requirements file
    install_requires=[x.strip() for x in content]
)
