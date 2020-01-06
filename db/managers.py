from itertools import dropwhile, filterfalse

from django_no_sql.db.functions import Functions
from django_no_sql.db.queryset import Query, QuerySet


class Manager(Functions):
    """A class that regroups all the base functionnalities for
    interracting with the database
    """
    def __init__(self, data=None):
        self.db_data = data

    def insert(self, **kwargs):
        pass
    
    def _all(self):
        """Get all the records of the database"""
        # return QuerySet(self.db_data)
        return self.db_data

    def include(self, *fields):
        """Get only certain fields based on their key"""
        new_record_to_return = {}
        new_queryset = []

        for record in self.values():
            for key, value in record.items():
                # Here we check that the key is not
                # present in the fields that the user
                # does not want
                if key in fields:
                    new_record_to_return.update({key: value})
            new_queryset.append(new_record_to_return)
            # We reset this parameter just
            # in case. Previous values can't
            # linger in and cause issues
            new_record_to_return = {}
        return QuerySet(new_queryset)

    def exclude(self, *fields):
        """Get certain fields by excluding those that you do need"""
        new_record_to_return = {}
        new_queryset = []

        for record in self.values():
            for key, value in record.items():
                # Here we check that the key is not
                # present in the fields that the user
                # does not want
                if key not in fields:
                    new_record_to_return.update({key: value})
            new_queryset.append(new_record_to_return)
            # We reset this parameter just
            # in case. Previous values can't
            # linger in and cause issues
            new_record_to_return = {}
        return QuerySet(new_queryset)

    def get(self, **query):
        """Get a single item from the database
        """
        if 'id' in query:
            # If the user passes a single numeric
            # item, then we can return on item
            if not isinstance(query['id'], list):
                return self.get_by_id(int(query['id']))
            else:
                # Otherwise, if we get a list or a tuple,
                # it means we need to return multiple items
                pass
        return self.iterator(**query)

    def get_rand(self, n, **query):
        """Get a random amount of records based on n and
        the parameters of your filter
        """

        def get_random_record(records):
            import random
            return random.choice(records)

        random_records = []

        for _ in range(0, n):
            random_records.append(get_random_record(self.values()))
        if query:
            # When the user adds a filter to query the random
            # records, call the iterator
            return self.iterator(data=random_records, **query)
        return random_records

    def get_or_create(self, **kwargs):
        available_fields = self.available_keys()
        base_structure = dict()
        base_structure.update({available_field for available_field in available_fields})

    def _filter(self, **query):
        """Retrieve data based on a list of filters"""
        return QuerySet(self.iterator(**query))

    def delete(self, **kwargs):
        pass

    def select_related(self, *keys):
        pass

    def values(self):
        """Return the items of the database as an array of dictionnaries"""
        return [data for data in self.db_data.values()]

    @classmethod
    def limit(cls, n, **kwargs):
        return cls.filter(**kwargs)[:n]

    def first(self):
        """Return the first value of the database"""
        return self.values()[0]

    def last(self):
        """Return the last value of the database"""
        return self.values()[-1]

    def count(self):
        """Return the number of items in the database"""
        return len(self.values())

    @classmethod
    def as_manager(cls, data=None):
        """Instantiates the manager once again and
        returns the class
        """
        return cls(data=data)
