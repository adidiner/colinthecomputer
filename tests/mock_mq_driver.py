message_box = {}

def task_publish(message, host, port, *, segment):
	if not message_box[segment]:
		message_box[segment] = []
	message_box[segment].append(message)

def share_publish(message, host, port, *, topic, segment):
	if not message_box[segment]:
		message_box[segment] = []
	message_box[segment].append((topic, message))

def task_consume(on_message, host, port, topic, segment):
	