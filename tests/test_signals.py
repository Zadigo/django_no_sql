import unittest

database = Database(path_or_url=PATH)
database.load_database()

@database.before_save()
def celebrity_change(instance):
    print(instance)

class TestSignals(unittest.TestCase):
    def test_can_connect(self):
        pass