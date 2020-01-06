# from django_api.db.database import Database, A
# from django_api.db.queryset import QuerySet
# from django_api.db.operators import OR, AND, When, Annotate, F
# from django_api.db.fields import CharField
# from django_api.db.operators import Avg

from django_no_sql.db.database import Database, A
from django_no_sql.db.queryset import QuerySet

# PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_api\\db\\database.json'
# database = Database(path_or_url=PATH)

# TESTS
# r = database.right_hand_filter('names__name__eq', {'names': {'name': 'Kendall'}})
# r = database.right_hand_filter('name', {'name': F('name')})
# print(r)

# ALL
# qs = database.manager._all()

# GET
# qs = database.manager.get(surname='Jenner')
# database.manager.get(surname__name='Jenner')
# qs = database.manager.get(location__country='USA')
# database.manager.get(location='USA')
# qs = database.manager.get_or_create(surname='Jenner')
# qs = database.manager.get(id=2)
# qs = database.manager.get(id=8)
# qs = database.manager.get(age__lt=24)
# qs = database.manager.get(age__gt=24)
# qs = database.manager.get(age__eq=22)
# qs = database.manager.get(age__ne=22)
# qs = database.manager.get(age__lte=22)
# qs = database.manager.get(age__gte=22)
# qs = database.manager.get(age=22)
# qs = database.manager.get(name__contains='Hai')
# qs = database.manager.get(name__exact='Hailey')
# qs = database.manager.get_rand(1)

# FILTER
# qs = database.manager.filter(surname='Jenner')
# qs = database.manager.filter(surname__contains='Je')
# qs = database.manager.filter(surname__contains='Ken')
# qs = database.manager.exclude('name')
# qs = database.manager.include('name', 'location')
# qs = database.manager.filter(height__gt=175)
# qs = database.manager.filter(height__gte=168, age__gt=22)
# qs = database.manager._filter(Avg('age'))

# SPECIAL
# qs = database.manager.count()

# QUERYSET
# qs = QuerySet(database.db_data)
# e = qs.limit(2)
# e = qs.first()
# e = qs.last()

# Functions
# print(F('name'))
# qs = database.manager.get(name=F('Kendall'))

# database.create('Something', ['Celebrities'], ['name', 'surname', 'age'])

# print(qs.values())
# print(e)


# class Celebrity(A):
#     name = CharField(45, blank=True, null=True)
#     surname = CharField(45, blank=True, null=True)

#     # def __str__(self):
#     #     return self.name

# print(Celebrity())

# from django.db.models.query import F


# print(qs)
