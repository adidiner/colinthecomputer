[![Build Status](https://travis-ci.org/adidiner/colin-the-computer.svg?branch=master)](https://travis-ci.org/adidiner/colin-the-computer)
[![codecov](https://codecov.io/gh/adidiner/colin-the-computer/branch/master/graph/badge.svg)](https://codecov.io/gh/adidiner/colin-the-computer)

# Colin The Computer

A project for Advanced System Design course, simulating a Brain Computer Interface. See [full documentation](https://colin-the-computer.readthedocs.io/en/latest).

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Usage](#usage)
    - [The Client](#the-client)
    - [The Server](#the-server)
        - [The Publisher](#the-publisher)
    - [The Parsers](#the-parsers)
    - [The Saver](#the-saver)
    - [The API](#the-api)
    - [The CLI](#the-cli)
    - [The GUI](#the-gui)

## Installation

TODO

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:adidiner/colin-the-computer.git
    ...
    $ cd colin-the-computer/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [colin] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Basic Usage

TODO

## Usage

The `colinthecomputer` package consists of 7 subpackages:
- [The Client](#the-client)
- [The Server](#the-server)
- [The Parsers](#the-parsers)
- [The Saver](#the-saver)
- [The API](#the-api)
- [The CLI](#the-cli)
- [The GUI](#the-gui)

### The Client

Available as `colinthecomputer.client`.

Provides the following function:

- `upload_sample`
    Used to read and upload a snapshots sample to the server.

    ```pycon
    >>> from cortex.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    … # upload path to host:port
    ```

The client also provides the following CLI:

```sh
$ python -m cortex.client upload-sample \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'snapshot.mind.gz'
…
```

### The Server

Available as `colinthecomputer.server`.

Provides the following function:

- `run_server`
    Runs the server in a given address. 
    The server recieves snapshots from client connection, and uses a passed publish function to publish them.
    Use the [Publisher](#the-publisher) to obtain a publishing function to the message queue.

The server also provides the following CLI:

```sh
$ python -m cortex.server run-server \
      -h/--host '127.0.0.1'          \
      -p/--port 8000                 \
      'rabbitmq://127.0.0.1:5672/'
```

The `run-server` command recieves a URL to a message queue, which the server will publish the recieved snapshots to.
The URL is of the form `'mq://host:port`.

#### The Publisher

TODO (should this even be here?)

### The Parsers

Available as `colinthecomputer.parsers`

Provides the following function:

- `run_parser`
    Runs a parser to a given field, parsing raw data as consumed from the message queue (a.k.a the snapshots published by the server), and returns the result.

    ```pycon
    >>> from cortex.parsers import run_parser
    >>> data = … 
    >>> result = run_parser('pose', data)
    ```