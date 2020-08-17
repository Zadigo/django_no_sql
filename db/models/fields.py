import datetime
import importlib
import re

from django import forms
from django.core import checks, exceptions, validators

from django_no_sql.db.errors import FieldError, ValidatorError


class Field:
    """This is the base field class for all the fields available
    to implement in a model"""

    default_error_messages = {
        'null': 'This field cannot be null',
        'blank': 'This field cannot be blank'
    }

    def __init__(self, max_length=None, default=None, description=None,
                name=None, verbose_name=None, validators:list=None, help_text=None,
                choices=(), nested_in=None, editable=True, primary_key=False):
        self.max_length = max_length
        self.default = default
        self.description = description
        self.name = name
        self.verbose_name = verbose_name
        self.validators = validators
        self.help_text = help_text
        self.choices = choices
        self.editable = editable
        self.primary_key = primary_key

        self.auto_now = False
        self.auto_now_add = False

        self.null = False
        self.empty = False

        self.choices = None        

        # This parameter is specific to fields
        # that are nested in others such as:
        # {location: {city: "", address: ""}}
        self.nested_in = nested_in    

        self.base_format = {'type': None, 'null': self.null, 'empty': self.empty}

        if self.default:
            self.base_format.update({'default': self.default})
        # Always verify what elements are passed
        # in the kwargs here
        # self.kwargs = self.check_kwargs(kwargs)

        # Uses definitions passed by the user
        # to the field in order to validate
        # the values that will be passed to
        # store in field
        # self.validators = self.validate()

        # self.base_format['verbose_name'] = verbose_name
        # self.base_format['max_length'] = max_length
        # self.base_format['description'] = description

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__str__()})'

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return str(self.base_format)

    @property
    def as_dict(self):
        """Return the field as dictionnary for the JSON file"""
        return self.base_format

    @property
    def cannot_be_empty(self):
        """Check if the field can be empty"""
        return True if self.empty else False

    @property
    def cannot_be_null(self):
        """Check if the field can be null"""
        return True if self.null else False

    @staticmethod
    def cannot_be_null_and_empty(self):
        return all([self.cannot_be_null, self.cannot_be_empty])
    
    def set_names(self, name):
        """Sets the name components for the fields"""
        self.name = name
        if not self.verbose_name:
            self.verbose_name = name.replace('_', ' ')

    def before_save(self):
        """Resolves the value of a field before storing it
        to the database. This is useful for date fields
        for example or 
        """
        pass

    def to_python(self, value):
        """Resolves the value of a field extracted from the database
        to a python object"""
        return value

    def formfield(self, **kwargs):
        return kwargs

    def check(self):
        """A definition that checks the paramaters and their validity
        such as the name, null, description..."""
        return [
            self._check_name()
        ]

    def _check_name(self):
        if self.name.endswith('_'):
            return [
                checks.Error(
                    'This is an error',
                    obj=self
                )
            ]
        elif self.name == 'pk':
            return [
                checks.Error(
                    "",
                    obj=self
                )
            ]

    def _check_validators(self, **kwargs):
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

    def do_validators(self, value):
        """Runs the value against all the provided validators
        """
        errors = []
        if self.validators and not self.editable:
            for validator in self.validators:
                try:
                    validator(value)
                except exceptions.ValidationError:
                    errors.extend('error')

            if errors:
                raise exceptions.ValidationError(errors)
        return value

    def validate(self, value):
        if not self.editable:
            return

        if self.null and value is None:
            pass

        if self.empty and value == '':
            pass

        if self.choices is not None:
            pass

    def clean(self, value):
        """Runs all the validation steps in order
        to save the value to the database"""
        value = self.to_python(value)
        self.do_validators(value)
        self.clean(value)
        return value
                

class IntegerField(Field):
    """Field for integers"""
    def __init__(self, minimum=None, maximum=None, verbose_name=None, validators:list=None):
        super().__init__(verbose_name=verbose_name)
        self.base_format['type'] = 'integer'
        if maximum is not None:
            self.base_format['maximum'] = maximum
        if minimum is not None:
            self.base_format['minimum'] = minimum

    # def validate(self, **kwargs):
    #     if self.minimum or self.maximum:
    #         if not isinstance(self.minimum, int) or not isinstance(self.maximum, int):
    #             raise FieldError(f'{self.minimum or self.maximum} should be an integer.')

    #         # Make sure that the minimum number
    #         # does not exceed the maximum one,
    #         # otherwise this would not make sense
    #         if self.minimum >= self.maximum:
    #             raise FieldError(f'The minimum number is superior or equal to the maximum number.')
            
    #         if self.maximum <= self.minimum:
    #             raise FieldError(f'The maximum number is inferior or equal to the minimum number.')

    #         if 'exclusive_minimum' in kwargs:
    #             self.base_format['exclusive_minimum'] = kwargs['exclusive_minimum']
            
    #         if 'exclusive_maximum' in kwargs:
    #             self.base_format['exclusive_maximum'] = kwargs['exclusive_maximum']

    #         self.base_format['minimum'] = self.minimum
    #         self.base_format['maximum'] = self.maximum

    def to_python(self, integer):
        if not isinstance(integer, int):
            raise Exception()
        return int(integer)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.IntegerField,
            **kwargs
        })

class PositiveIntegerField(IntegerField):
    """A field that can only hold a positive integer"""
    def __init__(self):
        super().__init__(minimum=0)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 0,
            **kwargs
        })

class DecimalField(IntegerField):
    """Field for decimals or floats"""
    def validate(self, number):
        if not isinstance(number, float):
            raise Exception()
        return number

class CharField(Field):
    """A basic character field"""
    def __init__(self, max_length, **kwargs):
        super().__init__(max_length=max_length, **kwargs)
        self.base_format['type'] = 'string'

    def to_python(self, value):
        if isinstance(value, str) or value is None:
            return value
        return str(value)


class TextField(CharField):
    """Field for lengthier text"""
    pass


class URLField(CharField):
    """Field for storing URLS"""
    def __init__(self, name=None, verbose_name=None):
        default_validators = [validators.URLValidator]
        super().__init__(200, name=name, verbose_name=verbose_name)
        self.base_format['type'] = 'url'

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.URLField,
            **kwargs
        })


class FilePathField(Field):
    """Base field for storing files"""
    def __init__(self):
        super().__init__()
        self.base_format = {'type': 'file'}


class ArrayField(Field):
    """Field for storing array type data"""
    def __init__(self):
        super().__init__()
        self.base_format = {'type': 'array'}

    def validate(self, value):
        if not isinstance(value, list):
            raise Exception()
        return value


class DateField(Field):
    def __init__(self, auto_now=False, auto_now_add=False):
        super().__init__()
        self.base_format = {'type': 'date'}
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

        # Loads the datetime module
        self.date_module = importlib.import_module('datetime', \
                                 package='datetime.datetime')

    def before_save(self):
        """Resolves a date before saving it to the database"""
        if self.auto_now or self.auto_now_add:
            d = self.date_module.datetime.now().date()
            # self.default = d
            self.base_format['default'] = str(d)

    def before_load(self, d):
        """Resolves a date before extracting it from the database"""
        return self.date_module.datetime.strptime(d, '%Y-%m-%d')


class DateTimeField(DateField):
    pass


class TimeField(Field):
    pass


class BooleanField(Field):
    def __init__(self):
        super().__init__(default='False')

    def validate(self, boolean):
        if not isinstance(boolean, bool):
            raise Exception()
        return boolean


class ObjectField(Field):
    pass


class AutoField(IntegerField):
    def __init__(self):
        super().__init__(minimum=1)
        self.base_format.update({'type': 'integer'})


class BinaryField(Field):
    pass


class CommaSeparatedField(Field):
    def __init__(self):
        super().__init__()

    def validate(self, s):
        is_match = re.match(r'[\w+\,]+', s)
        if not is_match:
            raise Exception()
        return s


class SlugField(Field):
    def validate(self, s):
        is_match = re.match(r'[\w+\-]+', s)
        if not is_match:
            raise Exception()
        return s

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.SlugField,
            **kwargs
        })


class EmailField(Field):
    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.EmailField, 
            **kwargs
        })


class ChoicesField(Field):
    def __init__(self):
        super().__init__()
        self.base_format.update({'type': 'choices'})

    def to_python(self):
        pass
# print(ChoicesField())
