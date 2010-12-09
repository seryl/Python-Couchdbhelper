from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='couchdbhelper',
      version=version,
      description="Python Couchdb helper functions",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python couchdb helper',
      author='Josh Toft',
      author_email='joshtoft@gmail.com',
      url='https://github.com/seryl/Python-Couchdbhelper',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "couchdb"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
