from django_no_sql.db.aggregates import (Avg, Max, Min, Mode, Spread,
                                         STDeviation, Sum, Variance)
from django_no_sql.db.database import Database
from django_no_sql.db.functions import F, Functions, Case, When
from django_no_sql.db.models import fields, models
from django_no_sql.db.operators import Operators
from django_no_sql.db.queryset import QuerySet
from django_no_sql.db import backends
import timeit

# TESTDATA = {
#     '1': {'name': 'Kendall', 'surname': 'Jenner', 'details': {'age': 25}},
#     '2': {'name': 'Kendall', 'surname': 'Olisa', 'details': {'age': 28}},
#     '3': {'name': 'Hailey', 'surname': 'Baldwin', 'details': {'age': 23}},
#     '4': {'name': 'Selena', 'surname': 'Gomez', 'details': {'age': 21}},
# }

start = timeit.default_timer()

VALUES = [
    {'name': 'Kendall', 'surname': 'Jenner', 'details': {'age': 25}},
    {'name': 'Kendall', 'surname': 'Olisa', 'details': {'age': 28}},
    {'name': 'Hailey', 'surname': 'Baldwin', 'details': {'age': 23}},
    {'name': 'Selena', 'surname': 'Gomez', 'details': {'age': 21}},
]

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\database.json'

# database = Database(path_or_url=PATH)
database = Database(import_name=__file__)
raw_data = database.load_database()

first_record = database.manager.first()
# When calling last after a first queryset
# was run, it returns the last item of the
# already populated queryset whereas in this
# configuration, it should return the last
# item of the database data
# FIX: The copy of the manager always
# includes new queryset and never the
# new db database when the new queryset
# does not exist
# FIX2: The copy includes the previous
# version of the manager -> first()
last_record = database.manager.last()

all_values = database.manager.all()
record = database.manager.get(name='Kendall')
record = database.manager.get(age__eq=22)
# s = database.manager.get(name__re=r'[Kk]en\w+')
print(record)


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
# s = f.resolve(data=VALUES)
# s = f.field
# s = f.functions.last_id()
# s = f.resolved_values
# s = f > 14
# s = f == 24
# s = f * 2
# s = f - 6
# print(s)


# database = Database(path_or_url='C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\test.json')
# # database.override_oncreate = True
# def age_validator(age):
#     if age == 22:
#         raise ValueError('Value should not be 22')
#     return age
# fields_to_create = {
#     'name': fields.CharField(45),
#     'surname': fields.CharField(45),
#     'age': fields.IntegerField(minimum=15, maximum=99, validators=[age_validator])
# }
# # fields_to_create = [
# #     fields.CharField(45),
# #     fields.CharField(45)
# # ]
# database.create_inline('Celebrity', fields_to_create=fields_to_create)
# print(database.loaded_json_data)
# s = database.db_name
# s = database.db_data
# s = database.records
# s = database.field_names
# s = database.model_fields
# s = database.model_name
# s = database.transform_data()
# s = database.manager.values()
# s = database.manager.filter(age__gt=F('age') - 5)
# s = database.manager._all()
# print(s)



# class Image(models.Model):
#     name = fields.CharField(145)
#     surname = fields.CharField(135)
#     age = fields.IntegerField(minimum=35)

#     # class Meta:
#     #     abstract = True
#     #     plural = 'Celebritites'
#     #     proxy = False

# i = Image()
# i.database.migrate()
# s = i.manager.filter(name='Kendall')
# s = i.database
# print(s)

# print(s)

# import timeit
# a = timeit.timeit()
# celebrity = Celebrity()
# s = celebrity.manager.count()
# s = celebrity.manager.count()
# # image = Image()
# print(celebrity.database.field_names)
# b = timeit.timeit()
# # print(image.database.field_names)



# s = STDeviation('age')
# s([{'age': 15}, {'age': 22}, {'age': 22}])
# print(s)

# o = Operators('age=15', 'age=20')


# v = Variance('age')
# v.resolve([{'age': 15}, {'age': 16}])
# print(v.result)

# print(AND('name=Kendall', 'age__eq=22', 'surname=Jenner'))
# print(AND('name=Kendall', 'age__eq=22', 'surname=Jenner').resolve([{'name': 'Kendall'}, {'name': 'Kylie'}]))
# print(XOR('value=google'))


# s = Min('attributes__height')
# w = s.resolve([{'age': 15, 'attributes': {'height': 167}}, {'age': '45', 'attributes': {'height': 187}}])
# print(s)

# f = F('age')
# w = f.resolve([{'age': 15, 'attributes': {'height': 167}}, {'age': 45, 'attributes': {'height': 187}}])
# w = f.resolve([{'age': 15, 'attributes': {'height': 167}}])
# w = f.resolve([{'age': 15, 'attributes': {'height': 167}}], for_save=True)
# z = f + 4
# print(w)

# e = AND('age__gt=15', 'age__lt=19')
# print(e & e)
# print(e.field_objects[0].sign)

# a = Sum('age')
# print(a)


# o = Operators('age__location')
# print(o.field_objects)


# queryset = QuerySet(query=VALUES)
# queryset = QuerySet(db_instance=database)
# s = queryset.functions.db_data
# s = queryset.functions.new_queryset
# s = queryset.copy()


# Backends
# data = backends.file_reader(PATH)
# data_to_put = {
#     "name": "Sophie",
#     "surname": "Turner",
#     "age": 27,
#     "height": 176,
#     "location": {
#         "country": "ENG",
#         "state": "Essex",
#         "city": "London"
#     }
# }
# data = backends.update_database(PATH, data_to_put)
# print(data)

# def age_validator(age):
#     if age > 21:
#         return age
#     else:
#         raise ValueError('Age should be greater than 13')

# def test_validator(age):
#     if age == 22:
#         raise ValueError('Age should not be 22')

# Constraints
# value = database._check_constraint('age', 34)
# value = database._check_constraint('name', 'Kendall Jenner Paradise Circus')
# value = database._check_constraint('age', 22, [age_validator, test_validator])
# .. Using Django validators
# from django.core import validators as v
# value = database._check_constraint('age', 22, validators=[v.MaxLengthValidator])
# print(value)

# query = [{'name': 'Kendall', 'age': 28}, {'name': 'Hailey', 'age': 25}, {'name': 'Mariah', 'age': 28}, {'name': 'Pauline', 'age': 35}]
# condition1 = When(age__gte=23, then='old')
# condition2 = When(age__lt=23, then='young')
# # print(condition1(queryset=query))
# # print(condition2(queryset=query))
# # case = Case(condition1)
# # print(case(query))
# values = database.manager.annotate(age=Case(condition1, condition2))
# print(values)

# print('Finished in:', round(timeit.default_timer() - start, 4), 'seconds')
