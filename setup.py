#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(name='freealchemist',
      version='0.7',
      setup_requires='setuptools',
      description='FreeAlchemist is a figure block game written in Python where you have to connect blocks',
      author='Davide Gessa',
      author_email='gessadavide@gmail.com',
      url='https://github.com/dakk/FreeAlchemist',
      packages=['freealchemist'],
      install_requires=open('requirements.txt', 'r').read().split('\n'),
      entry_points={
          'console_scripts': [
              'freealchemist=freealchemist.main:main',
          ],
      },
      package_data={'freealchemist': ['media/*.png']},
      include_package_data=True,
      license='GPLv2',
      )
