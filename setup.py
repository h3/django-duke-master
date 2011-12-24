#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
django-duke-master
~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 Motion Média, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

VERSION = __import__('dukemaster').VERSION

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

install_requires = [
    # webserver
    'python-daemon>=1.6',
    'eventlet>=0.9.15',
    'simplejson',
    'South',
    'django-grappelli'
]

try:
    __import__('uuid')
except ImportError:
    # uuid ensures compatibility with older versions of Python
    install_requires.append('uuid')

#tests_require = [
   #'Django>=1.4,<1.5',
   #'django-celery',
   #'logbook',
   #'nose',
   #'unittest2',
#]

setup(
    name='dukemaster',
    version=VERSION,
    author='Maxime Haineault',
    author_email='max@motion-m.ca',
    url='https://github.com/h3/django-duke-master',
    description = 'Duke master server',
    long_description=__doc__,
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    license='BSD',
    install_requires=install_requires,
    dependency_links=[
    'https://github.com/fetzig/django-grappelli/tarball/master#egg=django-grappelli',
    ],
   #tests_require=tests_require,
   #extras_require={'test': tests_require},
   #test_suite='nose.collector',
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'duke-master = scripts.runner:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)


