class ResponseFailure:
    def __init__(self, code, message):
        self.code = code
        self.message = self._format_message(message)

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return "{}: {}".format(
                msg.__class__.__name__, "{}".format(msg)
            )
        return msg

    @property
    def value(self):
        return {"code": self.code, "message": self.message}

    def __bool__(self):
        return False


class ResponseSuccess:
    def __init__(self, value=None):
        self.code = 200
        self.value = value

    def __bool__(self):
        return True


def build_response_from_invalid_request(invalid_request):
    message = "\n".join(
        [
            f'{err["parameter"]}: {err["message"]}' for err in invalid_request.errors
        ]
    )
    return ResponseFailure(code=400, message=message)
