import io


def to_stream(data):
    if type(data) is io.BytesIO:
        return data
    return io.BytesIO(data)
