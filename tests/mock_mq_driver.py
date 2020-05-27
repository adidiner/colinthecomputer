message_box = {}


def task_publish(message, host, port, *, segment):
    if segment not in message_box:
        message_box[segment] = []
    message_box[segment].append(message)


def share_publish(message, host, port, *, topic, segment):
    if segment not in message_box:
        message_box[segment] = []
    message_box[segment].append((topic, message))


def task_consume(on_message, host, port, topic, segment):
    for message in message_box[segment]:
        on_message(topic, message)


def share_consume(on_message, host, port, topics, segment):
    for (topic, message) in message_box[segment]:
        if topic in topics:
            on_message(topic, message)
