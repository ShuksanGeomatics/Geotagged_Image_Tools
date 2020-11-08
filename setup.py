#!/usr/bin/env python
from setuptools import setup
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = os.path.join(thelibFolder,'requirements.txt')
install_requires = [] 
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
        
        
setup(name='geotagged_image_tools',
      version='0.1.0',
      description='Python installation script for Geotagged Image Tools',
      author='Gerry Gabrisch',
      author_email='gerry@shuksangeomatics.com',
      license='MIT',
      packages=['geotagged_image_tools'],
      requires=['Pillow', 'simplekml']
      )