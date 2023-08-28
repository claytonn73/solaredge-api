

class OctopusError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class APIKeyError(OctopusError):
    def __init__(self, product):
        super().__init__("{} requires authorisation and no key provided.".format(product))
