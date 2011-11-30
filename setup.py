#!/usr/bin/env python

from distutils.core import setup

setup(name='fabric_bricks',
      version='0.1',
      description='Fabric Bricks',
      author='German Krauss',
      author_email='german@devartis.com',
      url='www.devartis.com',
      packages=['fabric_bricks', 'fabric_bricks.apache', 'fabric_bricks.deploy',
          'fabric_bricks.dev', 'fabric_bricks.django', 'fabric_bricks.mysql',
          'fabric_bricks.nginx', 'fabric_bricks.pip', 'fabric_bricks.project',
          'fabric_bricks.slice', 'fabric_bricks.sqlite', 'fabric_bricks.svn',
          'fabric_bricks.virtualenv'],
     )
