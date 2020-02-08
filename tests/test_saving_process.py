import unittest

# Observations:
# 1. We can access the manager in a circular way
# which can cause some issues e.g.
# database.manager.db_instance.manager?
# >> Maybe maybe insert the manager instance
# >> in the database instance in the Manager __init__?

# 2. Find a technique to refresh the data from the
# database once it is saved


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
    {'name': 'Taylor'},
    {'name': 'Julie'}
]

class Functions:
    db_data = None
    new_queryset = []

    def iterator(self, name=None):
        if self.new_queryset:
            self.new_queryset = [record for record in self.new_queryset if record['name'] == name]
        else:
            self.new_queryset = [record for record in self.db_data if record['name'] == name]
        return self.new_queryset

class QuerySet:
    functions = Functions()

    def __init__(self, db_instance=None, query=None):
        if db_instance:
            # self.db_instance = db_instance
            self.functions.db_data = db_instance.loaded_json_data
        else:
            self.functions.new_queryset = query

    def copy(self):
        klass = self.__class__(query=self.functions.new_queryset)
        return klass

    def __repr__(self):
        return str(self.functions.db_data)

class Manager(QuerySet):
    def __init__(self, db_instance=None, query=None):
        if db_instance:
            # By doing this, we are creating a
            # recursion where .database.manager.db_instance.manager...,
            # gets createsd. There should really be a better option?
            self.db_instance = db_instance

            super().__init__(db_instance=db_instance)
        else:
            super().__init__(query=query)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.functions.new_queryset})'

    def __len__(self):
        return len(self.functions.new_queryset)

    def create(self, data_to_save):
        return self.db_instance.save(data_to_save)

class Database:
    loaded_json_data = {}

    required_keys = ['name']

    def load_database(self):
        self.loaded_json_data = self.transform(DATA)
        self.set_database_class(data_to_use=self.loaded_json_data)

    def set_database_class(self, data_to_use=None):
        self.manager = Manager(db_instance=self)

    @staticmethod
    def transform(records):
        return [record for record in records.values()]

    def last_item_id(self, increment=False):
        number_of_items = len(self.loaded_json_data)
        return number_of_items + 1 - 1 if increment else number_of_items

    def check_required_keys(self, using_data):
        errors = []
        for required_key in self.required_keys:
            if required_key not in using_data:
                errors.append(required_key)
        if errors:
            iterated_keys = ', '.join(self.required_keys)
            raise Exception(f'The following keys "{iterated_keys}" are required before saving.')

    def save(self, data_to_save):
        self.check_required_keys(data_to_save)
        self.loaded_json_data.append(data_to_save)
        return {f'{self.last_item_id(increment=True)}': data_to_save}


database = Database()
database.load_database()
created_data = database.manager.create({'name': 'Julie'})
print(created_data)

# class TestSavingProcess(unittest.TestCase):
#     def setUp(self):
#         self.database = Database()
#         self.database.load_database()

#     def test_saving_process(self):
#         saved_data = self.database.manager.insert({'name': 'Julie'})
#         self.assertListEqual(self.database.loaded_json_data, EXPECTED_DATA)
#         self.assertEqual(len(self.database.loaded_json_data), 6)
#         self.assertDictEqual(self.database.loaded_json_data[-1], {'name': 'Julie'})

# if __name__ == "__main__":
#     unittest.main()

#     # suite = unittest.TestSuite()
#     # suite.addTest(TestDatabase('test_loaded_data'))
#     # runner = unittest.TextTestRunner()
#     # runner.run(suite)