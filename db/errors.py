class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class SchemaError(DatabaseError):
    pass

class FieldError(DatabaseError):
    pass

class ValidatorError(DatabaseError):
    pass

class FilterError(DatabaseError):
    """Raises an error when a special keyword is erroneous"""
    def __init__(self, message, f):
        self.f = f
        self.message = message + f' Received: {self.f}'

class KeyExistError(DatabaseError):
    """A specific error for when a key the user tries to query does not exist"""
    def __init__(self, key, keys):
        self.message = 'The key (%s) that you are trying to get does not exist. Available keys are: %s' % (key, keys)

class ItemExistError(DatabaseError):
    """An error for when an item does not exist in the database"""
    def __init__(self, reference):
        self.message = 'The item with id "%s" does not exist in your database' % reference

class SubDictError(DatabaseError):
    def __init__(self, f, subdict, **kwargs):
        first_key = list(subdict.keys())[0]
        self.message = '"%s" filter returned a subdictionnary.\
        You should push your filter to query that. For example: %s__%s' % (f, f, first_key)

    def __str__(self):
        return self.message