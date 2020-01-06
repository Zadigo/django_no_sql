"""This module regroups a set of wrapper classes that can
be used implement additional functionalities to the records
that are retrieved from the database.
"""
from itertools import dropwhile, takewhile, filterfalse

class Query:
    """A wrapper class for data retrieved from the database"""
    def __init__(self, data):
        self.data = data

    def resolve_field(self, field):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}({self.data})'

    def __str__(self):
        return str(self.data)

    def __unicode__(self):
        return self.__str__()

    def __getitem__(self, index):
        return self.data[index]

class QuerySet(Query):
    """An extended wrapper for multiple records"""
    def values(self):
        """Return the items of the database as an array of dictionnaries"""
        # If the data we receive is already a list,
        # then we can just return the data without
        # any iteration whatsoever
        if isinstance(self.data, list):
            return self.data
        if isinstance(self.data, dict):
            return [self.data]
        return [data for data in self.data]

    def limit(self, n):
        """Return a list of items"""
        return self.values()[:n]

    def count(self):
        """Return the number of items in the database"""
        return len(self.values())

    def last(self):
        """Return the last item of the queryset"""
        return self.values()[-1]

    def first(self):
        """Return the first item of the queryset"""
        return self.values()[0]

    def update(self, **kwargs):
        pass

    def update_or_create(self, **kwargs):
        pass

    def available_keys(self):
        return self.data.keys()
