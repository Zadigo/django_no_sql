from collections import OrderedDict

from django_no_sql.db.functions import Functions
from django_no_sql.db.queryset import QuerySet


class Manager(QuerySet):
    """A Manager is the main interface that implements functions for
    running queries on the database

    Description
    -----------

        The Manager returns a copy of a queryset in most situations which
        allows for added querying on the data
    
    Parameters
    ----------
    
        db_instance: corresponds to the instance of the database that is
        calling or implementing the manager
        
        query: represents a sub dictionnary of a data that you want to query
        using the manager
    """
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
        """Clears the inner queryset of the Manager"""
        if self.has_queryset:
            self.functions.new_queryset = []
        return self

    @property
    def has_queryset(self):
        """Checks if the Manager has a current queryset"""
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
        """Get a specific item"""
        copy = self.copy()
        copy.functions.iterator(**expressions)
        if len(copy.functions.new_queryset) > 1:
            raise Exception(f"Received too many values. Got {len(copy.functions.new_queryset)}. You should use filter instead in such as filter({expressions})")
        return copy.functions.new_queryset

    def count(self):
        """Return the number of items in the queryset"""
        copy = self.copy()
        if copy.functions.new_queryset:
            return len(copy.functions.new_queryset)
        return len([])

    def first(self):
        """Return the first item of the queryset"""
        copy = self.copy()
        copy.functions.new_queryset = copy.functions.new_queryset[:1]
        return copy

    def last(self):
        """Return the last item of the queryset"""
        copy = self.copy()
        copy.functions.new_queryset = copy.functions.new_queryset[-1]
        return copy

    def exclude(self, *fields):
        """Run a query only on a specific set of fields"""
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
        """Run a query only on a specific set of fields"""
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

    def annotate(self, *functions, **aliases):
        """
        Annotates each record within a queryset with
        a new field with the function that was passed
        """
        copy = self.copy()
        query = copy.functions.new_queryset if copy.functions.new_queryset else copy.functions.db_data
        records = []
        if functions:
            for function in functions:
                function(query)

        if aliases:
            for name, case in aliases.items():
                case.name = name
                records.append(case(query))
        return records

    def aggregate(self, *args):
        copy = self.copy()
        results = []
        for klass in args:
            results.append(klass(copy.functions.new_queryset))
        if len(results) == 1:
            return results[0]
        return results

    def values_list(self, *fields, flat=True):
        # BUG: When calling one of the definitions
        # internlly e.g. from this class, we get a
        # the queryset + manager queryset both
        # together
        pass
