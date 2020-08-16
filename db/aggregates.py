import math
from collections import Counter

from django_no_sql.db.functions import F


class Aggregate(type):
    def __new__(cls, name, bases, cls_dict):
        new_class = super().__new__(cls, name, bases, cls_dict)
        return new_class


class Math(metaclass=Aggregate):
    function_type = None

    def __init__(self, field):
        self.field = field
        self.resolved_values = []

    def __call__(self, db_instance):
        f = F(self.field)
        # f.resolve(data=[{'age': 15}, {'age': 22}, {'age': 22}])
        f.resolve(data=db_instance)
        # self.resolved_values = f.resolved_values
        self.resolved_values = f.resolved_values
        return self.__str__()

    def __repr__(self):
        if not self.resolved_values:
            return f'{self.__class__.__name__}(False)'
        result = {f'{self.field}__{self.function_type}': self.calculate(self.resolved_values)}
        return f'{self.__class__.__name__}({result})'

    def __str__(self):
        return {f'{self.field}__{self.function_type}': self.calculate(self.resolved_values)}

    def calculate(self, values:list):
        """Empty method that performs a set of calculation
        and is overrident by the subclasses"""
        return False


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
    average_type = 'regular'

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
