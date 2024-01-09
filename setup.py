#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages
from setuptools import setup


with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()

requirements = (
    "Click>=8.1.7",
    "aiohttp>=3.8.6",
    "more-itertools>=10.1.0",
    "pip>=22",
    "tqdm>=4.66.1",
)

test_requirements = (
    "isort>=5.12.0",
    "pre-commit>=3.4.0",
    "pytest>=7.4.2",
)

dev_requirements = (
    "Sphinx>=1.8.5",
    "black>=23.9.1",
    "bump2version>=1.0.1",
    "coverage>=7.3.2",
    "flake8>=6.1.0",
    "pip>=22.3.1",
    "tox>=4.11.3",
    "twine>=4.0.2",
    "watchdog>=3.0.0",
    "wheel>=0.33.6",
)


setup(
    author="danny crasto",
    author_email="danwald79@gmail.com",
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Uses coroutines to download files",
    entry_points={
        "console_scripts": [
            "async_download=async_download.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="async_download",
    name="async_download",
    packages=find_packages(include=["async_download", "async_download.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    extras_require={
        "dev": dev_requirements,
        "testing": test_requirements,
    },
    url="https://github.com/danwald/async_download",
    version="1.4.0",
    zip_safe=False,
)
