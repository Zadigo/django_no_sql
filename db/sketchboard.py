from django_no_sql.db.managers import Manager
from django_no_sql.db.aggregates import Sum, Avg, Count, Min

manager = Manager(query=[{'name': 'Kendall Jenner', 'age': 21}, {
                  'name': 'Kendall Jenner', 'age': 21}])
w = manager.aggregate(Sum('age'), Avg('age'), Min('age'), Count('age'))
print(w)
