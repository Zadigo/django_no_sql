from django_no_sql.db.operators import F
import unittest

TESTDATA = [
    {
        "age": 15,
        "attributes": {
            "height": 187
        }
    }
]

class TestF(unittest.TestCase):
    def setUp(self):
        self.age = F('age')
        self.attributes = F('attributes__height')

    def test_field(self):
        self.assertEqual(self.age.field, 'age')
        self.assertEqual(self.attributes.field, 'attributes__height')

    def test_resolve_values(self):
        self.age.resolve(data=TESTDATA)
        self.assertIsInstance(self.age.resolved_values, list)

    def test_resolve_data(self):
        age = self.age.resolve(data=TESTDATA)
        self.assertIsInstance(age, list)
        self.assertEqual(15, age[0])

        attributes = self.attributes.resolve(data=TESTDATA)
        self.assertIsInstance(attributes, list)
        self.assertEqual(187, attributes[0])

    def test_length(self):
        self.age.resolve(data=TESTDATA)
        self.assertEqual(self.age.__len__(), 1)

    def test_add_one(self):
        # Testing the fact of adding one
        # to the F function instance:
        # f = F(age) -> f + 1
        self.age.resolve(data=TESTDATA)
        new_value = self.age + 1
        self.assertEqual(new_value, [16])

if __name__ == "__main__":
    unittest.main()