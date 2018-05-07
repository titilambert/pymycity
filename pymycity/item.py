from datetime import date

class Item():

    def __init__(self, title, start, end=None, location=None, url=None, all_day=False, description=None, metadata=None):
        self.title = title
        self.start = start
        self.end = end
        self.location = location
        self.url = url
        self._all_day = all_day
        self.description = description
        self.metadata = metadata
        if self.metadata is None:
            self.metadata = {}

    @property
    def all_day(self):
        if isinstance(self.start, date) and isinstance(self.end, date):
            return True
        return self._all_day
