#!/usr/bin/env python
#! coding: utf-8

from distutils.core import setup

version = __import__('fabric_bricks').__version__

setup(name='fabric_bricks',
      version=version,
      description='Fabric Bricks',
      author='German Krauss',
      author_email='german@devartis.com',
      url='http://guthub.com/devartis/fabric_bricks',
      packages=['fabric_bricks', 'fabric_bricks.apache', 'fabric_bricks.git',
          'fabric_bricks.dev', 'fabric_bricks.django_tasks', 'fabric_bricks.mysql',
          'fabric_bricks.nginx', 'fabric_bricks.pip', 'fabric_bricks.project',
          'fabric_bricks.slice', 'fabric_bricks.sqlite', 'fabric_bricks.svn',
          'fabric_bricks.virtualenv'],
     )
