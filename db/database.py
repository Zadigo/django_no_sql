import collections
import datetime
import functools
import json
import os
import secrets
from importlib import import_module

from django_no_sql.db import backends
from django_no_sql.db import errors as django_no_sql_errors
from django_no_sql.db.managers import Manager


class Database:
    """
    Main representation and entrypoint for a
    JSON database file
    """

    data_types = {
        'CharField': 'string',
        'IntegerField': 'integer',
        'BooleanField': 'number',
        'ArrayField': 'array',
        'ObjectField': 'object',
        'NullField': 'null'
    }

    loaded_json_data = []
    created_from_model = False
    database_loaded = False

    model_fields = []
    field_names = []

    # This is the main registry for storing
    # fields that should not be empty, null
    # or both empty and null
    required_fields = {'empty': [], 'null': [], 'both': []}

    _default_manager = None

    def __init__(self, path_or_url=None):
        self.path_or_url = path_or_url

        # NOTE: This section overrides the other path
        # checking by raising an overall error when the
        # .json file does not exist
        # if not os.path.exists(self.path_or_url):
        #     raise django_no_sql_errors.DatabaseError('The specified database does not exist')

    def __getattr__(self, name):
        # When we try to use the manager
        # without loading the database
        # before hand, we cannot access
        # the manager property. In which
        # case we need to raise a more
        # convinient error
        if name == 'manager':
            if not self.database_loaded:
                raise django_no_sql_errors.ManagerLoadingError()
        return name

    def load_database(self, key=None):
        """
        Opens the local database. This definition
        automatically calls the _check_schema in
        order to certify database integrity
        
        Parameters
        ----------
        
            key: The main entrypoint to your database data
        """
        # with open(self.path_or_url, 'r', encoding='utf-8') as db:
        #     try:
        #         raw_data = json.load(db)
        #     except json.JSONDecodeError:
        #         raise django_no_sql_errors.DatabaseError('The file that was opened is empty.')
        #     if not raw_data:
        #         raise django_no_sql_errors.NoSchemaError()
        raw_data = backends.file_reader(self.path_or_url)
        self._check_schema(raw_data)
        self.database_loaded = True
        self.loaded_json_data = self.transform_data(raw_data, key=key)
        self.set_database_class(data_to_use=raw_data)
        return raw_data

    def set_database_class(self, data_to_use=None, **kwargs):
        """
        Defines the different properties of the class with
        the key parameters of the database
        
        Properties
        ----------

            Data_to_use: The data of the current JSON file to
            use to initialize the Database, the Manager and 
            its QuerySet
        """
        field_errors = []

        if 'title' in data_to_use:
            self.model_name = data_to_use['title']
        else:
            field_errors.append('title')

        if 'properties' in data_to_use:
            properties = data_to_use['properties']
            if properties and not self.model_fields and not self.field_names:
                # Even if the database was not constructed from a model,
                # consider it to be the base. Hence why we still populate
                # self.model_fields in order to simplify the process
                self.model_fields = [prop for prop in properties.values()]
                self.field_names = properties.keys()
        else:
            field_errors.append('properties')

        self.required_fields = data_to_use['required'] if 'required' in data_to_use else []
        
        # Map the fields that require a value and
        # cannot be empty, null or both
        for field in self.model_fields:
            # Models pass class type fields where
            # as the normal Database instance
            # pass dictionnaries
            if not isinstance(field, dict):
                if field.cannot_be_null:
                    self.required_fields['null'].append(field)
                elif field.cannot_be_empty:
                    self.required_fields['empty'].append(field)
                elif field.cannot_be_null and field.cannot_be_empty:
                    self.required_fields['both'].append(field)
            else:
                break

        if field_errors:
            raise django_no_sql_errors.DatabaseError(f'{field_errors} fields are not present in your database.')

        if not self.created_from_model and self.database_loaded:
            # try:
            #     # Attach a default manager to the newly
            #     # created database instance
            #     module = importlib.import_module('db.managers')
            # except:
            #     raise ImportError('Cannot attach a default manager to the database instance')
            # else:
            #     if module:
            #         module_dict = module.__dict__
            #         manager = module_dict['Manager'](db_instance=self)
            #         self._default_manager = manager

            # DEPRECATED: This will be replaced with
            # the import module technique above
            self.manager = Manager(db_instance=self)
    
        return True
    
    def _update_schema(self, schema, field, value):
        """Updates specific fields of the database schema
        
        Parameters
        ----------
            
            Schema: The database schema to use
            
            Field: The field to update
            
            Value: The value of the field to update
        """
        allowed_fields = ['title', 'version', 'properties']
        if field not in allowed_fields:
            pass

        with open(self.path_or_url, 'w', encoding='utf-8') as db:
            try:
                schema[field] = value
            except (KeyError, django_no_sql_errors.SchemaUpdataError):
                raise
            else:
                schema['version'] = schema['version'] + 1
                schema['modified_on'] = str(datetime.datetime.now())
                json.dump(schema, db, indent=4)
        return True

    def _check_schema(self, schema):
        """
        Checks that the provided schema is a valid one
        """
        return True

    def transform_data(self, raw_data, key=None, ordered_dict=False):
        """
        Transforms the data from the database into an list
        containing a series of dictionnaries for manageability.

        Description
        -----------

            In order to simplify iteration over the top dictionnary,
            storing each dict as an array does exactly that

        Parameters
        ----------

            raw_data: the original dabase data including schema

            key: The key of the data field in your database. Generally
            the name is "data" but you can override it here

            ordered_dict: return the transformed data as an ordered dict

        Example
        -------

            {1: {a: b}, 2: {c: d}} becomes [{a: b}, {c: d}]
        """ 
        if isinstance(self.db_data, list):
            return self.db_data
        if not key:
            key = 'data'
        return [record for record in raw_data[key].values()]

    def create_inline(self, model_name, fields_to_create:dict, **kwargs):
        """
        Create a database inline
        
        Example
        -------

            database = Database(path_or_url=/path/)
            database.create_inline(Celebrities, [CharField(...)])
        """
        self.field_names = list(fields_to_create.keys())
        self.model_fields = field_values = list(fields_to_create.values())
        return self.create_from_model(model_name, field_values, **kwargs)

    def create_from_model(self, model_name, fields_to_create:list, **kwargs):
        """
        Create a database from a Model class

        Example
        -------

            database = Database(path_or_utl=/path/)
            database.create_from_model(Celebrity, [...])
        """
        # constructed_database_path = os.path.join('', f'{model_name}.json')
        # os.path.exists(constructed_database_path)

        if not os.path.exists(self.path_or_url):
            with open(self.path_or_url, 'w', encoding='utf-8') as db:
                schema_structure = self._create_fields(self._create_default_schema(model_name), fields_to_create)
                json.dump(schema_structure, db, indent=4)
            return True
        else:
            # self.path_or_url = constructed_database_path
            # Otherwise, attempt to load the database 
            # and return its data
            self.load_database()
            # Check that the title of the model corresponds
            # the current Model class that is trying to
            # access the database model
            # if all_data['title'] == model_name:
            #     raise Exception('The current model does not exist in the database')
            return self.database_loaded

    def _create_fields(self, schema:dict, model_fields:list):
        """A definition that creates new properties fields in the schema
        
        Properties
        ----------
        
            schema: The schema to use
            
            model_fields: The fields as dictionnary to append to the properties
            section of the schema
        """
        required_fields = []
        # FIXME: When the database is created inline, the name of the field
        # is not passed. Either we pass the names of the fields within the
        # field class CharField(134, name='some name') or either we pass a
        # dict of fields {name: CharField(134)}
        for index, field in enumerate(self.field_names):
            field_properties = model_fields[index].as_dict
            if not any([field_properties['null'], field_properties['empty']]):
                required_fields.append(field)
            schema.update({'properties': {field: field_properties}})
        # new_fields = {field.as_dict['name']: field.as_dict for field in fields}
        schema.update({'required': required_fields})
        self.required_fields = required_fields
        return schema

    def _compare_fields(self, schema, model_fields:list):
        """Checks if the current fields from the database and the incoming
        fields from the model are the same. If not, it updates the
        model fields
        """
        # Current properties are field classes,
        # we have to render them as dictionnaries
        current_database_fields = [prop for prop in schema['properties'].values()]
        model_fields = [model_field.as_dict for model_field in model_fields]
        if not current_database_fields == model_fields:
            new_model_fields = {model_field['name']: model_field for model_field in model_fields}
            self._update_schema(schema, 'properties', new_model_fields)
            return True
        return False

    @staticmethod
    def _create_default_schema(model_name):
        """Returns the base structure for a schema"""
        base_schema_structure = {
            '$schema': 'http://json-schema.org/draft-07/schema',
            '$id': secrets.token_hex(nbytes=25),
            'title': model_name,
            'created_on': datetime.datetime.now().timestamp(),
            'modified_on': '',
            'version': 1,
            'data': {},
            'properties': {},
            'required': [],
            'dependencies': {}
        }
        return base_schema_structure

    def migrate(self):
        """Commits a new schema to the database"""
        loaded_data = self.load_database()
        print('Migration complete!')
        return self._compare_fields(loaded_data, self.model_fields)

    def save(self, commit=True):
        pass

    def _check_constraint(self, field, value, validators:list=[]):
        truth_array = []
        try:
            # First, we have to find the index
            # of the field that we are dealing with
            # in order to get its related constraint
            field_names = list(self.field_names)
            index = field_names.index(field)
        except ValueError:
            raise django_no_sql_errors.FieldError('The field you are trying to refer to '
                        'does not exist: %s' % field_names)
        else:
            constraint = self.model_fields[index]
            python_constraints = {
                'string': str,
                'integer': int,
                'object': dict
            }

            # Cases where the field is an instance of
            # a dict means that we are dealing with 
            # field that has nested fields within it.
            # We have to pick up these fields in order
            # to perform the constraint check.
            if isinstance(python_constraints[constraint['type']], dict):
                pass

            truth_array.append(isinstance(value, python_constraints[constraint['type']]))

            if 'minimum' in constraint:
                truth_array.append(value > constraint['minimum'])
                
            if 'maximum' in constraint:
                truth_array.append(value < constraint['maximum'])

            if 'maxLength' in constraint:
                truth_array.append(len(value) < constraint['maxLength'])

        if field in self.required_fields:
            if value is None:
                truth_array.append(False)
            else:
                truth_array.append(True)

        if validators:
            for validator in validators:
                if callable(validator):
                    # Call the validator by passing
                    # the value -; technically, a validator
                    # should return the value or raise somekind
                    # of error if it not valid
                    klass = validator(value)
                    try:
                        if klass:
                            # If Klass has something, then we can
                            # assume that this is a Django validator.
                            # Then call the .compare() method of the
                            # validator
                            # FIXME: Find a way to compare two valid
                            # values...
                            truth_array.append(klass.compare(value, 34))
                    except:
                        pass

        return all(truth_array)
    
    def before_save(self, **kwargs):
        """A signal that executes a set of operations before
        saving data to the database
        """
        def signal(func):
            # def connect(instance):
            try:
                func(self)
            except:
                raise TypeError(f'Your function "{func.__name__}" is missing an "instance" parameter.')
            print('Do something with the signal here')
            # return connect
        return signal

class LinkedDatabase(Database):
    """Create databases that are linked to one another
    by a one-to-many or one-to-one links"""
    inner_link = 'one-to-many'
    related_databases = []
    # This is the many dictionnary that
    # remembers the links between each
    # database e.g. {a: {type: onetomany, databases: [b, c]}}
    database_links = {}
    prefetch = True

    def load_database(self, keys:list=None):
        pass
