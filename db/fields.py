from django_no_sql.db.errors import FieldError, ValidatorError
import datetime

class Field:
    """This is the general field class for all the fields"""
    def __init__(self, max_length=None, verbose_name=None, validators:list=None, **kwargs):
        self.base_format = {
            'type': None
        }

        self.kwargs = self.check_kwargs(kwargs)

        # Uses definitions passed by the user
        # to the field in order to validate
        # the values that will be passed to
        # store in field
        # self.validators = self.validate()

        if verbose_name:
            self.base_format['verbose_name'] = verbose_name

        if max_length:
            self.base_format['max_length'] = max_length

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__str__()})'

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return str(self.base_format)

    @property
    def as_dict(self):
        return self.base_format

    def check_kwargs(self, values:dict):
        """Checks whether the keywords passed in kwargs are
        tolerated or not for __init__
        """
        return values

    def validate(self, **kwargs):
        """Returns the validated list of validators for a given field
        """
        validated = []
        if len(self.validators) > 0:
            for validator in self.validators:
                # Check that the validator is a
                # callable function
                if not callable(validator):
                    raise ValidatorError(f'Validators should be callables: {validator}')
                validated.append(validator)
            return validated

    def perform_validation(self):
        """When an object is about to be saved in the database, this definition
        is called in order to execute all neceassary validations in regards to
        its type or constraints related to the field
        """
        pass

class IntegerField(Field):
    """Field for integers"""
    def __init__(self, minimum=None, maximum=None, verbose_name=None, validators:list=None, **kwargs):
        super().__init__(verbose_name=verbose_name)
        self.base_format = {
            'type': 'integer'
        }

        if minimum or maximum:
            if not isinstance(minimum, int) or not isinstance(maximum, int):
                raise FieldError(f'{minimum or maximum} should be an integer.')

            # Make sure that the minimum number
            # does not exceed the maximum one,
            # otherwise this would not make sense
            if minimum >= maximum:
                raise FieldError(f'The minimum number is superior or equal to the maximum number: {minimum} >= {maximum}')
            
            if maximum <= minimum:
                raise FieldError(f'The maximum number is inferior or equal to the minimum number: {minimum} <= {maximum}')

            if 'exclusive_minimum' in kwargs:
                self.base_format['exclusive_minimum'] = kwargs['exclusive_minimum']
            
            if 'exclusive_maximum' in kwargs:
                self.base_format['exclusive_maximum'] = kwargs['exclusive_maximum']

            self.base_format['minimum'] = minimum
            self.base_format['maximum'] = maximum

class PositiveIntegerField(IntegerField):
    pass

class DecimalField(Field):
    """Field for decimals or floats"""
    pass

class CharField(Field):
    def __init__(self, max_length, verbose_name=None, validators:list=None, blank=False, null=False):
        super().__init__(max_length=max_length, verbose_name=None, validators=None, blank=False, null=False)
        self.base_format['type'] = 'string'

class TextField(CharField):
    """Field for lengthier text"""
    pass

class UrlField(Field):
    """Field for storing URLS"""
    def __init__(self):
        self.base_format = {
            'type': 'url'
        }

    def validate_url(self, validators: list=None):
        pass

class FileField(Field):
    pass

class ArrayField(Field):
    def __init__(self):
        self.base_format = {
            'type': 'array'
        }

class DateField(Field):
    def __init__(self):
        self.base_format = {
            'type': 'date',
            'example': datetime.datetime.now
        }

