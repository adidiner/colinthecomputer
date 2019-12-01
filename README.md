# Colin The Computer

A project for Advanced System Design course, simulating a Brain Computer Interface

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:Adidi1511/colin-the-computer.git
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
## Usage

The `colin` packages provides the following class:

- `Thought`

    This class represents a thought, which is defined by a user, a timestamp and the thought itself.

    It provides the `serialize` method to serialize the thought as bytes, and the `desrialize` class method to create a new thought object from a serilized thought.

    ```pycon
    >>> from colin import Thought
    >>> thought1 = Thought(1, datetime(2000, 1, 1, 12, 0), "I'm hungry")
	>>> thought1
	Thought(user_id=1, timestamp=datetime.datetime(2000, 1, 1, 12, 0), thought="I'm hungry")
	>>> print(thought1)
	[2000-01-01 12:00:00] user 1: I'm hungry
    >>> thought1.serialize()
	b"\x01\x00\x00\x00\x00\x00\x00\x00…"
	>>> thought2 = Thought.deserialize(_)
	>>> thought1 == thought2
	True
    ```

The package also provides the following functions:
- `run_server`

    This function runs a server in a given addres, which recieves serilized thoughts from users, and stores them in a given data directory.

    ```pycon
    >>> from colin import run_server
    >>> run_server(('127.0.0.1', 5000), 'data/')
    ```

- `upload_thought`

    This function uploads a thought (user id and thought) to a connection in a given address.

    ```pycon
    >>> from colin import upload_thought
    >>> upload_thought(('127.0.0.1', 5000), 1, "I'm hungery")
    ```
    If the upload time is for example [2000-01-01 12:00:00], the server from the previous example would write "I'm hungry" to /data/1/2000-01-01_12-00-00.txt

- `run_webserver`

    This function runs a webserver at a given address, serving the data from a given directory

    ```pycon
    >>> from colin import run_webserver
    >>> run_webserver(('127.0.0.1', 8000), 'data/')
    ```

THERE IS A CLI AS WELL HJDSIOD
