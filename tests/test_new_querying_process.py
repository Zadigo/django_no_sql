"""This is the most simplistic version of the whole Database
querying process for testing purposes
"""

import unittest

DATA = {
    '1': {'name': 'Kendall'},
    '2': {'name': 'Hailey'},
    '3': {'name': 'Taylor'},
    '4': {'name': 'Selena'},
    '5': {'name': 'Taylor'}
}

EXPECTED_DATA = [
    {'name': 'Kendall'},
    {'name': 'Hailey'},
    {'name': 'Taylor'},
    {'name': 'Selena'},
    {'name': 'Taylor'}
]




class Functions:
    def iterator(self, name=None):
        if self.new_queryset:
            self.new_queryset = [
                record for record in self.new_queryset if record['name'] == name]
        else:
            self.new_queryset = [
                record for record in self.db_data if record['name'] == name]
        return self.new_queryset


class QuerySet(Functions):
    query_cache = None

    def copy(self, query=None):
        klass = self.__class__(query=self.query_cache)
        klass.functions = Functions()
        return klass

    def __repr__(self):
        return str(self.query_cache)


class Manager(QuerySet):
    counter = 0
    
    def __init__(self, db_instance=None, query=None):
        loaded_json_data = None
        if db_instance:
            loaded_json_data = db_instance.loaded_json_data
        self.query = loaded_json_data or query

    def __repr__(self):
        return f'{self.__class__.__name__}({self.functions.new_queryset})'

    def __len__(self):
        return len(self.functions.new_queryset)

    def get(self):
        return self.query

    def filter(self, name=None):
        # 1. Create a copy
        copy = self.copy()
        # 2. Do the query
        copy.functions.iterator(name=name)
        # 3. Change the inner query of the Manager
        #    through new_queryset attribute
        copy.functions.iterator(name=name)
        # 4. Return the copy with the query
        return copy

    def query_another_here(self, name=None):
        copy = self.copy()
        copy.functions.iterator(name=name)
        return copy

    def clone(self):
        new_manager = EmptyManager()
        new_manager.__dict__ = self.__class__.__dict__.copy()
        new_manager.query = self.copy(query=self.query)
        new_manager.__name__ = Manager.__name__
        new_manager.__qualname__ = Manager.__qualname__
        new_manager.functions = Functions()
        return new_manager



class Database:
    loaded_json_data = {}
    _default_manager = None

    def load_database(self):
        self.loaded_json_data = self.transform(DATA)
        self.set_database_class(data_to_use=self.loaded_json_data)

    def set_database_class(self, data_to_use=None):
        self._default_manager = Manager(db_instance=self).clone()

    @staticmethod
    def transform(records):
        return [record for record in records.values()]

# database = Database()
# database.load_database()
# database._default_manager.get()


# import timeit
# import time
# import random
# database = Database()

# while True:
#     names = ['Kendall', 'Hailey', 'Taylor', 'Selena']
#     a = timeit.timeit()
#     database.load_database()
#     # query = database.manager.query_another_here(name='Kendall')
#     query = database.manager.query_another_here(name=random.choice(names))
#     b = timeit.timeit()
#     # query = database.manager.query_something_here(name='Kendall').query_another_here(name='Taylor')
#     print(query)
#     print('Done in:', a - b)
#     time.sleep(3)

# class TestProcess(unittest.TestCase):
#     def setUp(self):
#         self.database = Database()

#     @unittest.expectedFailure
#     def test_not_loaded_data(self):
#         self.assertIsNotNone(self.database.loaded_json_data)
#         # Cannot access data before loading database
#         self.assertEqual(self.database.loaded_json_data, EXPECTED_DATA)
#         # Cannot access manager before loading database
#         self.assertRaises(Exception, self.database.manager)

#     def test_loaded_data(self):
#         self.database.load_database()
#         # Can access data
#         self.assertEqual(self.database.loaded_json_data, EXPECTED_DATA)
#         # Can access manager
#         self.assertIsInstance(self.database.manager, Manager)

#     def test_data_from_manager(self):
#         self.database.load_database()
#         self.assertEqual(self.database.manager, EXPECTED_DATA)

#     def test_data_from_functions(self):
#         self.database.load_database()
#         # Access DATA from Functions
#         self.assertEqual(
#             self.database.manager.functions.db_data, EXPECTED_DATA)

#     def test_new_queryset_attribute(self):
#         self.database.load_database()
#         # This attribute should have one value
#         queryset = self.database.manager.query_something_here(name='Kendall')
#         self.assertIsNotNone(self.database.manager.functions.new_queryset)
#         self.assertIsInstance(
#             self.database.manager.functions.new_queryset, list)
#         self.assertListEqual(queryset.functions.new_queryset, [
#                              {'name': 'Kendall'}])
#         self.assertEqual(len(queryset), 1)

#     def test_query_call_from_manager(self):
#         self.database.load_database()
#         self.assertIsInstance(
#             self.database.manager.query_something_here(name='Kendall'), Manager)
#         self.assertIsInstance(
#             self.database.manager.query_something_here(name='Selena'), QuerySet)
#         # Return result from queries should be a copy of the QuerySet thus a class
#         self.assertNotIsInstance(
#             self.database.manager.query_something_here(name='Taylor'), list)

#     def test_query_call_chained(self):
#         self.database.load_database()
#         self.assertNotIsInstance(self.database.manager.query_something_here(
#             name='Kendall').query_another_here(name='Taylor'), list)

#     def test_instances(self):
#         self.database.load_database()
#         self.assertIsInstance(self.database.manager, Manager)

#     def test_queryset_process(self):
#         self.database.load_database()
#         self.assertIsInstance(
#             self.database.manager.query_something_here(name='Selena'), QuerySet)
#         self.assertIsInstance(
#             self.database.manager.query_something_here(name='Taylor'), Manager)


# if __name__ == "__main__":
#     unittest.main()

#     # suite = unittest.TestSuite()
#     # suite.addTest(TestDatabase('test_loaded_data'))
#     # runner = unittest.TextTestRunner()
#     # runner.run(suite)
