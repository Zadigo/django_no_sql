import re

from django_no_sql.db.errors import KeyExistError
from django_no_sql.db.functions import Functions


class Operators:
    """This class is a superclass for operations such AND, OR and
    Conditional queries on the data of the database.

    Description
    -----------

        Suppose want to do something like this: get the values
        where a = 1 or a = 2.
        
        We would use an Operator such as OR where
        .filter(OR(a=1, a=2)) would be resolved into a logical query
        for retrieving the data from the database

        The expressions of the operators are resolved within themselves
        and their data by the F function.

        These are done by the .resolve() and .evaluate_expressions() definitions.
    """
    # keys_dict = []
    # values_to_search = []
    # functions = Functions()
    # # filter_dict = dict()

    # def __init__(self, *args):
    #     self.args = args
    #     self.filter_items = []

    # def resolve(self, data):
    #     cases = []

    #     operator_type = self.filter_items[-1]
    #     if not operator_type:
    #         pass
        
    #     self.functions.db_data = data
    #     print(data)

    #     # for item in data:
    #     #     for filter_element in self.keys_dict:
    #     #         pass

    # def decompose(self, *args, operator=None):
    #     """Decompose each string into a dictionnary or a list
    #     of lists containing each items separately
    #     """
    #     for arg in args:
    #         parameter, value = arg.split('=')
    #         self.keys_dict.append(parameter)
    #         self.values_to_search.append(value)
    #         # self.filter_dict.update({parameter: value, 'operator': ''})
    #     return [self.keys_dict, self.values_to_search, operator]
    #     # return self.filter_dict
    
    # def __repr__(self):
    #     return f'<{self.__class__.__name__}: {self.filter_items}>'

    # def __unicode__(self):
    #     return self.__str__()

    # def __str__(self):
    #     return str(self.filter_items)
    functions = Functions()

    expressions = []
    searched_values = []

    key_expressions = ['gt', 'lt']

    def __init__(self, *expressions):
        # First, we separate the expressions
        # from their equal sign e.g. age=14
        # .. [age] [14]
        for expression in expressions:
            self.decompose(expression)

        # Second, if the decomposed expression
        # has a __ in it, we also have to decompose
        # these elements e.g. age__gt
        # .. [age, gt]
        decomposed_expressions = []
        for expression in self.expressions:
            decomposed_expressions.append(self.functions.simple_decompose(expression))
        
        # Finally, we can start working
        # the decomposed elements -; we first
        # create an array of row objects
        field_objects = []
        for decomposed_expression in decomposed_expressions:
            for expression in decomposed_expression:
                # When the item is a database field,
                # we an create an F object with it
                if expression not in self.key_expressions:
                    f_instance = F(expression)
                else:
                    # Otherwise, apply the sign to the
                    # global variable sign
                    f_instance.sign = expression
            # f_instance.resolve(data=[{'age': 16}])
            field_objects.append(f_instance)

        # Resolve the data for each object
        for field_object in field_objects:
            field_object.resolve(data=[{'age': 16}])

        self.field_objects = field_objects

    def decompose(self, expression):
        """Decomposes an expression based on the equals sign"""
        if '=' in expression:
            exp, value = expression.split('=')
            self.expressions.append(exp)
            self.searched_values.append(value)

    def evaluate_expressions(self, data=None, operator=None):
        """A function that evaluates the decomposed expressions
        in regards to the data that is passed here
        """
        pass

        
class When(Operators):
    def __init__(self, if_condition=None, then_condition=None, else_condition=None, **additional):
        first_condition = super().decompose(if_condition)
        self.query = first_condition

class F:
    """The F function is a class that resolves expressions for
    other function classes like Avg, Sum...

    Description
    -----------

        It has a standalone query resolver that returns either a
        specific value or a list of values

        The F function is extremely useful for doing equality,
        comparisions etc directly on a value.

        For example, let's say we have F(age) where age is equals
        to 24. We can do F(age) != 26 or F(age) == 25 -; or, if
        age is a list it returns a list of booleans.

        In other words, the F function represents the value in itself.
    """
    functions = Functions()
    sign = 'eq'

    def __init__(self, field):
        self.field = field
        self.resolved_values = []

    def resolve(self, data=None, for_save=False):
        """A function into which the database data can be passed
        in order for the function to operate

        Parameters
        ----------

            data: the data on which to iterate
        """
        copy_data = data.copy()
        self.functions.db_data = data

        for item in copy_data:
            keys = self.functions.simple_decompose(self.field)
            for key in keys:
                try:
                    item = item[key]
                except KeyExistError:
                    print(self.functions.available_keys())
                    raise
            self.resolved_values.append(item)

            # If the modified value is directly for saving
            # into the database, then we prepare the sequence
            if for_save:
                pass

        return self.resolved_values

    def __str__(self):
        return str(self.resolved_values)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.field})'
    
    def __eq__(self, value):
        print(value)

    def __ne__(self, value):
        pass

    def __gt__(self, value):
        truth_list = []
        for resolved_value in self.resolved_values:
            if resolved_value > value:
                truth_list.append(True)
            else:
                truth_list.append(False)
        return truth_list

    def __add__(self, a):
        """Addition of two F functions or an F function with an integer..."""
        if isinstance(a, F):
            return self.resolved_values + a.resolved_values
        return [value + a for value in self.resolved_values]

    def __len__(self):
        return len(self.resolved_values)




class AND(Operators):
    def __and__(self, f):
        for field in self.field_objects:
            pass

class OR(Operators):
    def __or__(self, f):
        pass






class Aggregate:
    function_type = 'aggregate'
    functions = Functions()

    def __init__(self, field):
        self.field = field
        self.result = None
        self.f = F(self.field)

    def resolve(self, data, function_type=None):
        """This is a specific resolver for the dataset in order
        to avoid calling data from the __init__
        """
        self.f.resolve(data=data)

        if function_type:
            self.function_type = function_type

        if self.function_type == 'sum':
            self.result = sum(self.f.resolved_values)

        if self.function_type == 'avg':
            self.result = sum(self.f.resolved_values) / self.f.__len__()

        if self.function_type == 'min':
            self.result = min(self.f.resolved_values)

        if self.function_type == 'max':
            self.result = max(self.f.resolved_values)

        return self.result

    def __repr__(self):
        return f'{self.__class__.__name__}({self.f.__class__.__name__}({self.field})={self.result})'

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__str__()

class Annotate(Aggregate):
    function_type = 'annotate'

class Avg(Aggregate):
    function_type = 'avg'

class WeightedAvg(Aggregate):
    def __init__(self, field, **weigth):
        pass

class Sum(Aggregate):
    function_type = 'sum'

class Variance(Aggregate):
    pass

class STDeviation(Aggregate):
    pass

class Min(Aggregate):
    function_type = 'min'

class Max(Aggregate):
    function_type = 'max'



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
# print(z)

e = AND('age__gt=15', 'age__lt=19')
# print(e & e)
print(e.field_objects[0].sign)
