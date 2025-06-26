def of(value):
    return Optional(value)


def empty():
    return Optional(None)


class Optional:

    def __init__(self, value):
        self.value = value

    def map(self, mapper):
        if self.is_empty():
            return Optional(None)
        return Optional(mapper(self.value))

    def get(self):
        return self.or_else_raise()

    def or_get(self, other):
        return other if self.is_empty() else self.value

    def or_else_get(self, other_provider):
        return other_provider() if self.is_empty() else self.value

    def or_else_raise(self):
        return self.or_else_raise_exception(Exception("Value is None"))

    def or_else_raise_exception(self, exception):
        if self.is_empty():
            raise exception
        return self.value

    def if_present(self, processor):
        if self.is_present():
            processor(self.value)

    def is_present(self):
        return self.value is not None

    def is_empty(self):
        return self.value is None
