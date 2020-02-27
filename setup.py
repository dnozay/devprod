#!/usr/bin/env python3
from setuptools import setup
from distutils.util import convert_path
import codecs

# Load version information
main_ns = {}
ver_path = convert_path('devprod/version.py')
with codecs.open(ver_path, 'rb', 'utf8') as ver_file:
    exec(ver_file.read(), main_ns)

# Load README.md
readme_path = convert_path('README.md')
with codecs.open(readme_path, 'rb', 'utf8') as readme_file:
    long_description = readme_file.read()


setup(
    author_email='damiennozay+github@gmail.com',
    author='Damien Nozay',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control',
    ],
    description='Tools & Hacks for developer productivity',
    entry_points={
        'console_scripts': [
            'devprod = devprod.cli:main',
        ]
    },
    include_package_data=True,
    install_requires=open('requirements.txt').read(),
    keywords=[
        'ci/cd',
        'continuous integration',
        'developer',
        'github',
        'hacks',
        'productivity',
        'semaphoreci',
    ],
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='devprod',
    packages=['devprod'],
    python_requires='>=3.6',
    setup_requires=['setuptools-git', 'wheel'],
    test_suite='tests',
    url='https://github.com/dnozay/devprod',
    version=main_ns['__version__'],
)
