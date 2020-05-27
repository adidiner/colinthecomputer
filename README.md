[![Build Status](https://travis-ci.org/adidiner/colin-the-computer.svg?branch=master)](https://travis-ci.org/adidiner/colin-the-computer)
[![codecov](https://codecov.io/gh/adidiner/colin-the-computer/branch/master/graph/badge.svg)](https://codecov.io/gh/adidiner/colin-the-computer)
[![Documentation Status](https://readthedocs.org/projects/colin-the-computer/badge/?version=latest)](https://colin-the-computer.readthedocs.io/en/latest/?badge=latest)

# Colin The Computer

A project for Advanced System Design course, simulating a Brain Computer Interface. See [full documentation](https://colin-the-computer.readthedocs.io/en/latest).

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Usage](#usage)
  - [The Client](#the-client)
  - [The Server](#the-server)
  - [The Parsers](#the-parsers)
  - [The Saver](#the-saver)
  - [The API](#the-api)
  - [The CLI](#the-cli)
  - [The GUI](#the-gui)
- [Sub Functionalities](#sub-functionalities)
  - [The Reader](#the-reader)
  - [The Publisher, Worker and Consumer](#the-publisher-worker-consumer)
  - [Drivers](#drivers)

## Installation

1. Clone the repository and enter it:

   ```sh
   $ git clone git@github.com:adidiner/colin-the-computer.git
   ...
   $ cd colin-the-computer/
   ```

2. Run the installation script and activate the virtual environment:

   ```sh
   $ scripts/install.sh
   ...
   $ source .env/bin/activate
   [colin] $ # you're good to go!
   ```

   **Notice**:

   If no `docker` is installed, please install `docker:>18.09.9` and `docker-compose>1.23.2` bedore you run the installtion script.

   You may use the supplied docker installation script, by running:

   ```sh
   $ scripts/install-docker.sh
   ...
   ```

3) To check that everything is working as expected, run the tests:

   ```sh
   $ scripts/run-tests.sh
   ...
   ```

## Basic Usage

To simply start everything up, you can use the `run-pipeline` script:

```
$ scripts/run-pipeline.sh
Starting pipeline...
...
Please wait a few moments for everything to load...
...
Run a client to start the pipeline
```

When everything is up, run a client

```sh
$ python -m colinthecomputer.client upload-sample 'test_sample.mind'
```

And checkout `localhost:8080` to see the uploaded sample.

To stop the pipeline, run:

```sh
$ scripts/stop-pipeline.sh
```

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

- ```sh
   python -m colinthecomputer.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
  ```

  Which accepts a path to some raw data as consumed from the message queue, and prints the result (can be redirected).

- ```sh
  python -m colinthecomputer.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
  ```

  Which runs the parser so it consumes raw data from the message queue, and publishes the results back to it.

The current available parsers are:

- `pose` - collects the snapshot's tranlation and rotation.

- `color_image` - collects the snapshot's raw color image data, and converts it to a `JPG` image.

- `depth_image` - collects the snapshot's raw depth image data, and creates a 2D heatmap representation, accessible as a `JPG` image.

- `feelings` - collects the snapshot's feelings.

To add a new parser, simply add a `parse_something` method with a `field` attribute.

See [Parsers](https://colin-the-computer.readthedocs.io/en/latest/colinthecomputer.parsers.html#module-colinthecomputer.parsers) for more information.

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
`sh $ python -m colinthecomputer.saver save \ -d/--database 'postgresql://colin:password@127.0.0.1:5432/colin' \ 'pose' \ 'pose.result'`

    Which accepts a topic and a path to parsed data, saving it to the database.

- ```sh
  $ python -m colinthecomputer.saver run-saver  \
    'postgresql://colin:password@127.0.0.1:5432/colin' \
    'rabbitmq://127.0.0.1:5672/'
  ```
  Which consumes the parsed data from the message queue, then saving it to the database.

### The API

A RESTful API exposing the data available in the database.
Available as `colinthecomputer.api`.

Provides the following function:

- `run_api_server`
  Runs the API server at a given address, serving from a given dataabase.

  ```pycon
  >>> run_api_server(
  ...     host = '127.0.0.1',
  ...     port = 5000,
  ...     database_url = 'postgresql://colin:password@127.0.0.1:5432/colin',
  ... )
  … # listen on host:port and serve data from database_url
  ```

The API also provides the following CLI:

```sh
$ python -m colinthecomputer.api run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 5000              \
      -d/--database 'postgresql://colin:password@127.0.0.1:5432/colin'
```

It exposes the following endpoints:

- `GET /users`
  The users list.

- `GET /users/user-id`
  The user's data.

- `GET /users/user-id/snapshots`
  The user's available snapshots.

- `GET /users/user-id/snapshots/snapshot-id`
  The snapshot's available results.

- `GET /users/user-id/snapshots/snapshot-id/result-name`
  The result data.

- `GET /users/user-id/snapshots/snapshot-id/color-image/data.jpg`
  Binary data, only for BLOBS.

### The CLI

The CLI consumes the API and reflects it.
Available as `colinthecomputer.cli`.

The provided CLI corresponds the API's endpoints, e.g

```sh
$ python -m colinthecomputer.cli get-users
…
$ python -m colinthecomputer.cli get-user 1
…
$ python -m colinthecomputer.cli get-snapshots 1
…
$ python -m colinthecomputer.cli get-snapshot 1 2
…
$ python -m colinthecomputer.cli get-result 1 2 'pose'
…
```

The commands receive `-h/--host` and `-p/--port` flags to configure the API's address.

The `get-result` command receives `-s/--save` flag, which receives a path to save the binary data to.

### The GUI

The GUI consumes the API and reflects it, in a user-friendly manner.
Available as `colinthecomputer.gui`.

Provides the following function:

- `run_server`
  Runs he GUI server in a given address.

  ```pycon
  >>> from colinthecomputer.gui import run_server
  >>> run_server(
  ...     host = '127.0.0.1',
  ...     port = 8080,
  ...     api_host = '127.0.0.1',
  ...     api_port = 5000,
  ... )
  ```

The GUI also provides the following CLI:

```sh
$ python -m colinthecomputer.gui run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 8080              \
      -H/--api-host '127.0.0.1'   \
      -P/--api-port 5000
```

## Sub Functionalities

Some of the components of `colinthecomputer` include a smaller utility, which can be used seperatly of the entire component.

These provide a more advanced usage of the package.

### The Reader

A reader which reads sample files, enabling iteration over the available snapshots.
Available as `colinthecomputer.client.reader`.

Provides the following utilities:

- `Reader`
  A reader class initialized by a path to the sample and the file format, then exposing iteration over the sample.

  ```pycon
  >>> from colinthecomputer.client.reader import Reader
  >>> reader = Reader('sample.mind', 'protobuf')
  >>> reader.user
  … # user infortmation
  >>> for snapshot in reader:
  ...     print(snapshot)
  … # prints full snapshot data
  ```

- `read`
  Receives the sample path and format, and prints the data (without binary data).

  ```pycon
  >>> from colinthecomputer.client.reader import read
  >>> read('sample.mind', 'protobuf')
  user 5: Yellow Guy, born June 19, 1955 (male)
  Snapshot from December 04, 2019 at 10:08:07.476000:
  pose: {
    "translation": {
      "x": -0.05,
      ...
  }
  color image: 1920x1080 image
  depth image: 224x172 image
  feelings: {
    "hunger": 0.5,
    ...
  }
  ```

### The Publisher, Worker and Consumer

These are utilities for working with the message queue, available as `colinthecomputer.server.publisher`, `colinthecomputer.parsers.worker`, `colinthecomputer.saver.consumer`.

Each provides a class `Publisher`, `Worker` and `Consumer` respectivaly, initialized with a `mq_url`.

- The `Publisher` provides the `publish(message)` method, publishing messages of the form `(result, raw_data)`, to raw_data and result sections respectively.
- The `Worker` provides the `work(parser, field)` method, consuming raw data and publishing back the parser's result to the result section.
- The `Consumer` provides the `consume(on_message, fields)` method, consuming results and performing `on_message` upon them.

These utilities can be used together sepratly from the `server`, `parsers` and `saver` to play with the message queue more freely.

### Drivers

The drivers include read drivers, message queue drivers and database drivers.

The drivers are automatically imported, so adding a new driver to the corresponding package will immediatly enable the support of the given format / meesage queue / database.

For more details, see [read drivers](https://colin-the-computer.readthedocs.io/en/latest/colinthecomputer.client.read_drivers.html), [message queue drivers](https://colin-the-computer.readthedocs.io/en/latest/colinthecomputer.mq_drivers.html), [database drivers](https://colin-the-computer.readthedocs.io/en/latest/colinthecomputer.db_drivers.html)
