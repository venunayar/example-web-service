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

# name from config file
NAME = cfg_dict['progname']
# version from config file
VERSION = cfg_dict['version']

setup(
    name=NAME,
    version=VERSION,
    description='Library Management Service (LMS)',
    license='PSF',
    author='Nayar Tutorials',
    author_email='tutorials@naar.org',
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
    # install packages from requirements file
    install_requires=[x.strip() for x in content]
)
