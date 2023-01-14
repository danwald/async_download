Async download
--------------

![download](https://img.shields.io/pypi/v/async_download.svg "download") ![travis](https://img.shields.io/travis/danwald/async_download.svg) ![documentation status](https://readthedocs.org/projects/async-download/badge/?version=latest)


Uses coroutines to download urls

Note: Greedy and built for speed. [10K cdn hosted urls; 0.5GB Total data; <5 minutes; M1 laptop]

Usage
-----

```
Usage: async_download [OPTIONS]

Options:
  --execute         required to do something
  --urls-file PATH  urls to download  [required]
  --data-dir PATH   directory to save downloads  [required]
  --help            Show this message and exit.

```

* Free software: MIT license
* Documentation: https://async-download.readthedocs.io.


Install & Run
-------------
```bash
pipx install async-download
async_download --help
```

Development
-----------
```bash
pip install -e .[dev]
make test
```

Credits
-------

This package was created with Cookiecutter and the `audreyr/cookiecutter-pypackage` project template.

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)

The main loop was taken from
- [A Twilio tuitorial](https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp)
