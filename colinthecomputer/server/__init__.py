"""
A server which accepts client connections,
receives the uploaded snapshots and publishes them to the message queue.
"""

from .server import run_server
