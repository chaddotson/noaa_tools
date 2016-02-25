class FailedToLoadNWSSameCodesMap(RuntimeError):
    def __init__(self, status_code):
        super(RuntimeError, self).__init__("Failed to load NWS same code map.  Status: {0}".format(status_code))
