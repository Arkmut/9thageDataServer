
class ObjectViewer(object):
    """
    Convert dict to obj for django template
    """
    def __init__(self, d):
        self.__dict__ = d