from itertools import dropwhile, filterfalse

from django_no_sql.db.functions import Functions, F
from django_no_sql.db.queryset import Query, QuerySet


class Manager:
    """A class that regroups all the base functionnalities for
    interracting with the database
    """
    def __init__(self, data=None, db_instance=None):
        if data and not db_instance:
            # If we do not have an instance,
            # we ave to create a new Functions
            # instance with the database data
            # so that the manager can function
            # correctly
            self.db_data = data
            functions = Functions()
            functions.db_data = self.db_data
            self.functions = functions

        
        elif not data and db_instance:
            # When we pass an instance of the
            # database, the db_data is already
            # avaible for the manager
            self.db_data = db_instance.db_data
            self.functions = db_instance
        
        elif data and db_instance:
            raise Exception('You provided both data to use and a Database instance. You should choose which one to use.')

    def insert(self, **kwargs):
        """Creates a new record in the database"""
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

    def get(self, **expression):
        """Get a single item from the database
        """
        if 'id' in expression:
            # If the user passes a single numeric
            # item, then we can return one item
            if not isinstance(expression['id'], list):
                return self.get_by_id(int(expression['id']))
            else:
                # Otherwise, if we get a list or a tuple,
                # it means we need to return multiple items
                pass
        return self.functions.iterator(**expression)

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
            return self.functions.iterator(data=random_records, **query)
        return random_records

    def get_or_create(self, **kwargs):
        available_fields = self.functions.available_keys()
        base_structure = dict()
        base_structure.update({available_field for available_field in available_fields})

    def _filter(self, **expression):
        """Retrieve data based on a list of filters"""
        return QuerySet(self.functions.iterator(**expression))

    def delete(self, **kwargs):
        pass

    def select_related(self, *keys):
        pass

    def values(self):
        """Return the items of the database as an array of dictionnaries"""
        # return [data for data in self.db_data.values()]
        return self.functions.transform_data()

    @classmethod
    def limit(cls, n, **kwargs):
        return cls._filter(**kwargs)[:n]

    def first(self):
        """Return the first value of the database"""
        return self.values()[0]

    def last(self):
        """Return the last value of the database"""
        return self.values()[-1]

    def count(self):
        """Return the number of items in the database"""
        return len(self.values())

    def something_test(self):
        return self.functions.something_test()