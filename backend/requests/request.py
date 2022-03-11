class InvalidRequest:
    def __init__(self):
        self.errors = []

    def add_error(self, param, message) -> None:
        self.errors.append({"parameter": param, "message": message})

    def has_error(self) -> bool:
        return len(self.errors) > 0

    def __bool__(self):
        return False


class ValidRequest:
   
    def __bool__(self):
        return True