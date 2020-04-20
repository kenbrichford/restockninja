class TagConvertor:
    regex = '[A-Z0-9]{7}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value