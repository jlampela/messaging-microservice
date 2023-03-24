from utils.errors import ServiceErrors


def correct_length(string):
    if len(string) > 500:
        raise ServiceErrors(400, "Message too long.")
    return string