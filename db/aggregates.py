# class Aggregate(type):
#     def __new__(cls, name, bases, cls_dict):
#         new_class = super().__new__(cls, name, bases, cls_dict)
#         if name != "Math":
#             # Create a base __init__ for each class in
#             # order to take the field to aggregate
#             def __init__(self, field): self.field = field
#             setattr(new_class, '__init__', __init__)

#             f = F(new_class.field)
#             resolved_values = f.resolve(data=[{'age': 15}, {'age': 16}])
            
#             # We have to find a way to pass the self of the 
#             # subclass instead of the cls of the meta
#             result = cls_dict['calculate'](cls, resolved_values)
            
            
#             setattr(new_class, 'resolved_values', resolved_values)
#             setattr(new_class, 'result', result)
#         return new_class

# class Math(metaclass=Aggregate):
#     field = None

#     # def __str__(self):
#     #     return str({f'__{self.function_type}': self.result})

# class Sum(Math):
#     function_type = 'sum'

#     def caculate(self, values:list):
#         return sum(values)

# class Avg(Math):
#     function_type = 'avg'

#     def calculate(self, values:list):
#         return sum(values) / len(values)



# class Aggregate:
#     function_type = 'aggregate'
#     functions = Functions()

#     def __init__(self, field):
#         self.field = field
#         self.result = None
#         self.f = F(self.field)

#     def resolve(self, data, function_type=None):
#         """This is a specific resolver for the dataset in order
#         to avoid calling data from the __init__
#         """
#         self.f.resolve(data=data)

#         if function_type:
#             self.function_type = function_type

#         if self.function_type == 'sum':
#             self.result = sum(self.f.resolved_values)

#         if self.function_type == 'avg':
#             self.result = sum(self.f.resolved_values) / len(self.f)

#         if self.function_type == 'min':
#             self.result = min(self.f.resolved_values)

#         if self.function_type == 'max':
#             self.result = max(self.f.resolved_values)

#         if self.function_type == 'variance':
#             self.result = None

#         return self.result

#     def __repr__(self):
#         return f'{self.__class__.__name__}({self.f.__class__.__name__}({self.field})={self.result})'

#     def __str__(self):
#         return str({f'{self.field}__{self.function_type}': self.result})

#     def __unicode__(self):
#         return self.__str__()

# class Annotate(Aggregate):
#     function_type = 'annotate'

# class Avg(Aggregate):
#     function_type = 'avg'

# class WeightedAvg(Aggregate):
#     def __init__(self, field, **weigth):
#         pass

# class Sum(Aggregate):
#     function_type = 'sum'

# class Variance(Aggregate):
#     function_type = 'variance'

#     def caculate(self, values:list=None):
#         """Calculates the variance of each values"""
#         average = Avg(self.field).result
#         if not values:
#             values = self.f.resolved_values
#         return [round(value - average, 5) for value in values]

# class STDeviation(Aggregate):
#     pass

# class Min(Aggregate):
#     function_type = 'min'

# class Max(Aggregate):
#     function_type = 'max'


# class OrderBy:
#     data = None

#     def __init__(self, descending=False):
#         pass
