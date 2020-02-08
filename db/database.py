import datetime
import json
import os
import secrets

from django_no_sql.db.errors import (DatabaseError, FieldError,
                                     ManagerLoadingError, PrimaryKeyError,
                                     SchemaError)
from django_no_sql.db.managers import Manager

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\database.json'

class Database:
    loaded_json_data = []
    created_from_model = False
    database_loaded = False

    model_fields = []
    field_names = []

    # Fields that can be null,
    # empty or both
    required_fields = {'empty': [], 'null': [], 'both': []}

    def __init__(self, path_or_url=None):
        self.path_or_url = path_or_url

    def __getattr__(self, name):
        # When we try to use the manager
        # without loading the database
        # before hand, we cannot access
        # the manager property. In which
        # case we need to raise a more
        # convinient error
        if name == 'manager':
            if not self.database_loaded:
                raise ManagerLoadingError()
        return name

    def load_database(self):
        """Opens the local database and automatically 
        calls the .check_schema()"""
        with open(self.path_or_url, 'r', encoding='utf-8') as db:
            raw_data = json.load(db)
            self.database_loaded = True
            self.loaded_json_data = self.transform_data(raw_data)
            self.set_database_class(data_to_use=raw_data)
        return raw_data

    def set_database_class(self, data_to_use=None, **kwargs):
        """Defines the the different properties of the class
        
        Properties
        ----------

            Data_to_use: The data of the current JSON file to
            use to initialize the Manager and QuerySet
        """
        field_errors = []

        if 'title' in data_to_use:
            self.model_name = data_to_use['title']
        else:
            field_errors.append('title')

        if 'properties' in data_to_use:
            properties = data_to_use['properties']
            if properties and not self.model_fields and not self.field_names:
                self.model_fields = [prop for prop in properties.values()]
                self.field_names = properties.keys()
        else:
            field_errors.append('properties')
        
        # Map the fields that require a value and
        # cannot be empty, null or both
        for field in self.model_fields:
            if field.cannot_be_null:
                self.required_fields['null'].append(field)
            elif field.cannot_be_empty:
                self.required_fields['empty'].append(field)
            elif not field.cannot_be_null and not field.cannot_be_empty:
                self.required_fields['both'].append(field)

        if not self.created_from_model and self.database_loaded:
            self.manager = Manager(db_instance=self)

        if field_errors:
            raise DatabaseError('%s fields are not present in your database.' % field_errors)
    
        return True
    
    def _update_schema(self, schema, field, value):
        """Updates specific fields of the database schema"""
        allowed_fields = ['title', 'version', 'properties']
        if field not in allowed_fields:
            pass
        with open(self.path_or_url, 'w', encoding='utf-8') as db:
            try:
                schema[field] = value
            except KeyError:
                raise
            else:
                schema['version'] = schema['version'] + 1
                schema['modified_on'] = str(datetime.datetime.now())
                json.dump(schema, db, indent=4)
        return True

    def transform_data(self, raw_data, key=None):
        """Transforms the data from the database into an list
        containing a series of dictionnaries for manageability.

        Description
        -----------

            In order to simplify iteration over the top dictionnary,
            storing each dict as an array does exactly that

        Parameters
        ----------

            Key: The key of the data field in your database. Generally
            the name is "data" but you can override it here

        Example
        -------

            {1: {a: b}, 2: {c: d}} becomes [{a: b}, {c: d}]
        """ 
        if isinstance(self.db_data, list):
            return self.db_data
        if not key:
            key = 'data'
        return [record for record in raw_data[key].values()]

    def create_from_model(self, model_name, fields_to_create:list, **kwargs):
        """Create a database from a set of models"""
        if not os.path.exists(self.path_or_url):
            # Creates the database here
            with open(self.path_or_url, 'w', encoding='utf-8') as db:
                schema_structure = {
                    "$schema": "http://json-schema.org/draft-07/schema",
                    "$id": secrets.token_hex(nbytes=25),
                    "title": model_name,
                    "created_on": datetime.datetime.now().timestamp(),
                    "modified_on": "",
                    "version": 1,
                    "data": {},
                    "properties": {}
                }
                schema_structure = self._create_fields(schema_structure, fields_to_create)
                json.dump(schema_structure, db, indent=4)
            return True
        else:
            # Otherwise, just load the database 
            # and return its data
            raw_data = self.load_database()
            # Check that the title of the model corresponds
            # the current Model class that is trying to
            # access the database model
            # if all_data['title'] == model_name:
            #     raise Exception('The current model does not exist in the database')
            return self.database_loaded

    @staticmethod
    def _create_fields(schema:dict, fields:list):
        """A definition that creates new properties fields in the JSON schema"""
        new_fields = {field.as_dict['name']: field.as_dict for field in fields}
        schema.update({'properties': new_fields})
        return schema

    def _compare_fields(self, schema, model_fields:list):
        """Checks if the current fields from the database and the incoming
        fields from the model are the same. If not, it updates the
        model fields"""
        # Current properties are field classes,
        # we have to render them as dictionnaries
        current_database_fields = [prop for prop in schema['properties'].values()]
        model_fields = [model_field.as_dict for model_field in model_fields]
        if not current_database_fields == model_fields:
            new_model_fields = {model_field['name']: model_field for model_field in model_fields}
            self._update_schema(schema, 'properties', new_model_fields)
            return True
        return False

    def migrate(self):
        loaded_data = self.load_database()
        print('Migration complete!')
        return self._compare_fields(loaded_data, self.model_fields)

    # @classmethod
    # def prepare_save(cls, data_to_save:dict=None):
    #     """Prepares the database and the data for saving before
    #     committing to the actual database

    #     Description
    #     -----------

    #     """
    #     key, values = data_to_save.items()
    #     if not isinstance(key, int):
    #         raise PrimaryKeyError(key)

    #     errors = []
    #     for key in values.keys():
    #         if key not cls.field_names:
    #             errors.append('%s is not a field of your model. Model fields are: ' % (key, ', '.join(cls.model_fields)))
    #             raise FieldError(errors)

    #     # Here we verify the type of the
    #     # values that want to passed to
    #     # the database in respect to the
    #     # properties stored
    #     validates = []
    #     for field in cls.model_fields:
    #         pass
        
    #     def commit(state=True):
    #         return data_to_save

    #     return commit

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
