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

A client which reads snapshots samples, uploading them to the server.
Available as `colinthecomputer.client`.

Provides the following function:

- `upload_sample`
    Used to read and upload a sample to the server.

    ```pycon
    >>> from colinthecomputer.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    … # upload path to host:port
    ```

The client also provides the following CLI:

```sh
$ python -m colinthecomputer.client upload-sample \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'snapshot.mind.gz'
…
```

### The Server

A server which acceptes client connections as mentioned above, and publishes the data to a message queue.
Available as `colinthecomputer.server`.

Provides the following function:

- `run_server`
    Runs the server in a given address. 
    The server recieves snapshots from client connection, and uses a passed publish function to publish them.
    Use the [Publisher](#the-publisher) to obtain a publishing function to the message queue.

The server also provides the following CLI:

```sh
$ python -m colinthecomputer.server run-server \
      -h/--host '127.0.0.1'          \
      -p/--port 8000                 \
      'rabbitmq://127.0.0.1:5672/'
```

The `run-server` command recieves a URL to a message queue, which the server will publish the recieved snapshots to.
The URL is of the form `'mq://host:port`.

#### The Publisher

TODO (should this even be here?)

### The Parsers

A collection of parsers which consumed raw data from the message queue, then publishing the results to this message queue.
Available as `colinthecomputer.parsers`

Provides the following function:

- `run_parser`
    Runs a parser to a given field, parsing raw data as consumed from the message queue (a.k.a the snapshots published by the server), and returns the result.

    ```pycon
    >>> from colinthecomputer.parsers import run_parser
    >>> data = … 
    >>> result = run_parser('pose', data)
    ```

The parsers also provides the following CLI:

- 
    ```sh
     python -m colinthecomputer.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
    ```

    Which accepts a path to some raw data as consumed from the message queue, and prints the result (can be redirected).

- 
    ```sh
    python -m colinthecomputer.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
    ```

    Which runs the parser so it consumes raw data from the message queue, and publishes the results back to it.

The current available parsers are:

- `pose`: collects the snapshot's tranlation and rotation.

- `color_image`: collects the snapshot's raw color image data, and converts it to a `JPG` image.

- `depth_image`: collects the snapshot's raw depth image data, and creates a 2D heatmap representation, accessible as a `JPG` image.

- `feelings`: collects the snapshot's feelings.

### The Saver

A saver which connects to a database, and parsed results to it.
Available as `colinthecomputer.server`

Provides the following class:

- `Saver`
    Initialized with a database URL of the form `db://username:password@host:port/db_name`.
    Provides the `save` function, receiving parsed data and its topic and saving it to the database.

    ```pycon
    >>> from colinthecomputer.saver import Saver
    >>> saver = Saver(database_url)
    >>> data = …
    >>> saver.save('pose', data)
    ```

The saver also provides the following CLI:

-
    ```sh
    $ python -m colinthecomputer.saver save                     \
          -d/--database 'postgresql://colin:password@127.0.0.1:5432/colin' \
         'pose'                                       \
         'pose.result'
    ```

    Which accepts a topic and a path to parsed data, saving it to the database.

- 
    ```sh
    $ python -m cortex.saver run-saver  \
      'postgresql://colin:password@127.0.0.1:5432/colin' \
      'rabbitmq://127.0.0.1:5672/'
    ```
    Which consumes the parsed data from the message queue, then saving it to the database.

### The API


