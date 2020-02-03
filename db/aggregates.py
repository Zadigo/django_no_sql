from django_no_sql.db.functions import F
import math
from collections import Counter

class Aggregate(type):
    def __new__(cls, name, bases, cls_dict):
        new_class = super().__new__(cls, name, bases, cls_dict)
        if name != "Math":
            pass
        return new_class

class Math(metaclass=Aggregate):
    function_type = None

    def __init__(self, field):
        f = F(field)
        f.resolve(data=[{'age': 15}, {'age': 22}, {'age': 22}])
        self.resolved_values = f.resolved_values
        self.result = {f'{field}__{self.function_type}': self.calculate(f.resolved_values)}

    def __str__(self):
        return str(self.result)

class Sum(Math):
    """Sums the values of the field"""
    function_type = 'sum'

    def calculate(self, values:list):
        return sum(values)

class Count(Math):
    """Counts the values of the field"""
    function_type = 'count'

    def calculate(self, values:list):
        return len(values)

class Avg(Math):
    """Average of the values of the field"""
    function_type = 'avg'

    def calculate(self, values:list):
        return sum(values) / Count.calculate(self, values)

class Variance(Math):
    function_type = 'variance'

    def calculate(self, values:list):
        total = 0
        count = Count.calculate(self, values)
        average = Avg.calculate(self, values)
        for value in values:
            total = total + (value - average)**2
        return total / count

class STDeviation(Math):
    function_type = 'st_dev'

    def calculate(self, values:list):
        v = Variance.calculate(self, values)
        return math.sqrt(v)

class Max(Math):
    """Maximum value of the field"""
    function_type = 'max'

    def calculate(self, values:list):
        return max(values)

class Min(Math):
    """Minimum value of the field"""
    function_type = 'min'

    def calculate(self, values:list):
        return min(values)

class Mode(Math):
    function_type = 'mode'

    def calculate(self, values:list):
        return Counter(values).most_common(1)

class Spread(Math):
    function_type = 'spread'
    
    def calculate(self, values:list):
        return Max.calculate(self, values) - Min.calculate(self, values)

class OrderBy:
    pass