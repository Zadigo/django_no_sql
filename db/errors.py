class DatabaseError(Exception):
    """Top level or global database error"""
    def __init__(self, message, **kwargs):
        self.message = message

    def __str__(self):
        return self.message

class SchemaError(DatabaseError):
    """Errors related to the structure of the JSON schema"""
    def __init__(self, fields):
        super().__init__(f'The following fields "{", ".join(fields)}" are missing from your schema.')

class FilterError(DatabaseError):
    """Raises an error when a special keyword is erroneous"""
    def __init__(self, message, f):
        self.f = f
        self.message = message + f' Received: {self.f}'

class KeyExistError(DatabaseError):
    """A specific error for when a key the user tries to query does not exist"""
    def __init__(self, key, keys):
        self.message = f'The key "{key}" that you are trying to get does not exist. Available keys are: {", ".join(keys)}.'

class ItemExistError(DatabaseError):
    """An error for when an item does not exist in the database"""
    def __init__(self):
        self.message = 'The item you are looking for does not exist in your database'

class SubDictError(DatabaseError):
    """When the returned value is a dictionnary as opposed to a value e.g. int, float..."""
    def __init__(self, f, subdict, **kwargs):
        first_key = list(subdict.keys())[0]
        message = '"%s" expression returned a subdictionnary. You should push your expression to ' \
                        'explore it further. For example: %s__%s' % (f, f, first_key)
        super().__init__(message)

class NullFieldError(DatabaseError):
    """Error raised when a models' field, 
    not considered as abstract, is None"""
    def __init__(self, model_name, field):
        super().__init__('"%s" is None while %s is not set to be used as an abstract Model.' % field, model_name)

class FieldError(DatabaseError):
    pass

class ValidatorError(DatabaseError):
    pass
