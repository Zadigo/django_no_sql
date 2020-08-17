import re

from django_no_sql.db.errors import KeyExistError
from django_no_sql.db.functions import Functions, F


class Operators:
    """This class is a superclass for operations such as AND, OR and
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

    key_expressions = ['gt', 'lt', 'gte', 'lte', 'eq']

    def __init__(self, *expressions):
        # First, we separate the expressions
        # from their equal sign e.g. age=14
        # .. [age] [14]
        for expression in expressions:
            decomposed_expressions = self.functions

        # Second, if the decomposed expression
        # has a __ in it, we also have to decompose
        # these elements e.g. age__gt
        # .. [age, gt]
        decomposed_expressions = [self.functions.simple_decompose(expression) \
                                    for expression in self.expressions]
        
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

    def __repr__(self):
        return str(self.field_objects)

# class AND(Operators):
#     def __and__(self, f):
#         # field = F(f)
#         # field.resolve(data=None)
#         decomposed_fields = [decomposed_field for field in self.field_objects]
#         print(decomposed_fields)

# class OR(Operators):
#     def __or__(self, f):
#         pass
