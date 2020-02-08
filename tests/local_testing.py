from django_no_sql.db.database import Database
from django_no_sql.db.fields import (CharField, DateField, IntegerField,
                                     URLField)
from django_no_sql.db.functions import F, Functions
from django_no_sql.db.models import Model
from django_no_sql.db.operators import Operators
from django_no_sql.db.aggregates import Sum, Avg, Variance, STDeviation, Min, Max, Mode, Spread
from django_no_sql.db.queryset import QuerySet

# TESTDATA = {
#     '1': {'name': 'Kendall', 'surname': 'Jenner', 'details': {'age': 25}},
#     '2': {'name': 'Kendall', 'surname': 'Olisa', 'details': {'age': 28}},
#     '3': {'name': 'Hailey', 'surname': 'Baldwin', 'details': {'age': 23}},
#     '4': {'name': 'Selena', 'surname': 'Gomez', 'details': {'age': 21}},
# }

VALUES = [
    {'name': 'Kendall', 'surname': 'Jenner', 'details': {'age': 25}},
    {'name': 'Kendall', 'surname': 'Olisa', 'details': {'age': 28}},
    {'name': 'Hailey', 'surname': 'Baldwin', 'details': {'age': 23}},
    {'name': 'Selena', 'surname': 'Gomez', 'details': {'age': 21}},
]

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\database.json'

# database = Database(path_or_url=PATH)
# database.load_database()
# data = database.manager.all().last()
# data['name'] = 'test'
# data.save()

# func = Functions()
# func.db_data = TESTDATA
# s = func.available_keys()
# s = func.available_keys(check_key='1')
# s = func.last_item_id
# s = func.auto_increment_last_id
# t = func.transform_data()
# s = func.simple_decompose('location__country')
# s = func.simple_decompose('location__country__age__other')

# s = func.decompose(age__gt=13, location__eq='Paris')
# s = func.keys_dict
# s = func.searched_values

# s = func.right_hand_filter('name__eq', {'name': 'Selena', 'surname': 'Gomez', 'details': {'age': 27}})
# e = func.right_hand_filter('details__age__eq', {'name': 'Selena', 'surname': 'Gomez', 'details': {'age': 27}})
# s = func.comparator(e[0], 25, special_keyword=e[1])
# s = func.iterator(data=t, details__age__gt=22, name='Kendall')
# s = func.iterator(data=t, name='Kendall', surname='Olisa')
# s = func.filter_by_ids([1, 2])



# f = F('details__age')
# f.resolve(data=VALUES)
# s = f.field
# s = f.functions.last_item_id
# s = f.resolved_values
# s = f > 14
# s = f == 24
# s = f * 2
# s = f - 6


# database = Database(path_or_url='C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\test.json')
# database = Database()
# database.override_on_create = True
# database.create('Celebrity', [CharField(145, name='age')])
# s = database.db_name
# s = database.db_data
# s = database.records
# s = database.field_names
# s = database.model_fields
# s = database.model_name
# s = database.transform_data()
# s = database.manager.values()
# s = database.manager._filter(age__gt=F('age') - 5)
# s = database.manager._all()
# print(s)



class Image(Model):
    name = CharField(145)
    surname = CharField(135)
    age = IntegerField(minimum=145)


    # class Meta:
    #     abstract = True
    #     plural = 'Celebritites'
    #     proxy = False

i = Image()
# i.database.migrate()
# s = i.manager.filter(name='Kendall')
s = i.database  

print(s)

# import timeit
# a = timeit.timeit()
# celebrity = Celebrity()
# s = celebrity.manager.count()
# s = celebrity.manager.count()
# # image = Image()
# print(celebrity.database.field_names)
# b = timeit.timeit()
# # print(image.database.field_names)

# path = 'C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\database.json'
# database = Database(path_or_url=path)
# database.load_database()
# s = database.manager.all()
# s = database.manager.values()
# s = database.manager.first()
# s = database.manager.get(name='Kendall')
# s = database.manager.get(age__eq=22)
# s = database.manager.insert()
# print(s)
# print(s)

