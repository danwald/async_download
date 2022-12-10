#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages
from setuptools import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = (
    'Click>=8',
    'aiohttp>=3.8',
    'tqdm>=4.64',
    'pip>=22',
)

test_requirements = (
    'isort>=5.10',
    'pre-commit>=2.20',
)

dev_requirements = (
    'pip>=22.3.1',
    'bump2version>=0.5.11',
    'wheel>=0.33.6',
    'watchdog>=0.9.0'
    'flake8>=3.7.8',
    'tox>=3.14.0'
    'coverage>-4.5.4',
    'Sphinx>=1.8.5',
    'twine>=1.14.0',
    'black>=21.7b0',
)


setup(
    author='danny crasto',
    author_email='danwald79@gmail.com',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description='Uses coroutines to download files',
    entry_points={
        'console_scripts': [
            'async_download=async_download.cli:main',
        ],
    },
    install_requires=requirements,
    license='MIT license',
    long_description_content_type='text/markdown',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='async_download',
    name='async_download',
    packages=find_packages(include=['async_download', 'async_download.*']),
    test_suite='tests',
    tests_require=test_requirements,
    extras_require={'dev': dev_requirements},
    url='https://github.com/danwald/async_download',
    version='1.2.0',
    zip_safe=False,
)
