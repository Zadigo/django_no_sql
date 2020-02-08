from itertools import dropwhile, filterfalse

from django_no_sql.db.functions import Functions
from django_no_sql.db.queryset import QuerySet

from collections import OrderedDict


class Manager(QuerySet):
    def __init__(self, db_instance=None, query=None):
        if db_instance:
            super().__init__(db_instance=db_instance)
        else:
            super().__init__(query=query)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.functions.new_queryset})'

    def __len__(self):
        return len(self.functions.new_queryset)

    def clear_inner_queryset(self):
        if self.has_queryset:
            self.functions.new_queryset = []
        return self

    @property
    def has_queryset(self):
        if self.functions.new_queryset:
            return True
        return False

    def all(self):
        copy = self.copy()
        copy.functions.new_queryset = copy.functions.db_data
        return copy

    def filter(self, **expressions):
        copy = self.copy()
        copy.functions.iterator(**expressions)
        return copy

    def get(self, **expressions):
        copy = self.copy()
        copy.functions.iterator(**expressions)
        if len(copy.functions.new_queryset) > 1:
            pass
        return copy

    def count(self):
        copy = self.copy()
        if copy.functions.new_queryset:
            return len(copy.functions.new_queryset)
        return len([])

    def first(self):
        copy = self.copy()
        copy.functions.new_queryset = copy.functions.new_queryset[:1]
        return copy

    def last(self):
        copy = self.copy()
        copy.functions.new_queryset = copy.functions.new_queryset[-1]
        return copy

    def exclude(self, *fields):
        copy = self.copy()
        constructed_record = {}
        new_queryset = []
        query = copy.functions.new_queryset if copy.functions.new_queryset \
                            else copy.functions.db_data
        for record in query:
            for key, value in record.items():
                if key not in fields:
                    constructed_record.update({key: value})
                    new_queryset.append(constructed_record)
            constructed_record = {}
        copy.functions.new_queryset = new_queryset
        return copy

    def include(self, *fields):
        copy = self.copy()
        constructed_record = {}
        new_queryset = []
        query = copy.functions.new_queryset if copy.functions.new_queryset \
                            else copy.functions.db_data
        for record in query:
            for key, value in record.items():
                if key in fields:
                    constructed_record.update({key: value})
                    new_queryset.append(constructed_record)
            constructed_record = {}
        copy.functions.new_queryset = new_queryset
        return copy
