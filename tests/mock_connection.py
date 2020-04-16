def create_mock_connection(receive_message):
	class MockConnection:
	    received_messages = []

	    def __init__(self, socket):
	        return

	    def __enter__(self):
	        return self

	    def __exit__(self, exception, error, traceback):
	        return

	    @classmethod
	    def connect(cls, host, port):
	        return MockConnection(None)

	    def send_message(self, message):
	        self.received_messages.append(message)

	    def receive_message(self):
	        return receive_message()

	    def close(self):
	        return
