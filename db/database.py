import datetime
import json
import os
import secrets

from django_no_sql.db.decorators import database_cache
from django_no_sql.db.errors import DatabaseError, SchemaError
from django_no_sql.db.fields import CharField
from django_no_sql.db.functions import Functions
from django_no_sql.db.managers import Manager
from django_no_sql.db.queryset import QuerySet


class Database(Functions):
    """This class is the main entrypoint for creating and doing
    actions on the database.

    The database is considered as the .json file that contain the 
    related schema, field properties and stored data.

    Description
    -----------

        There are many ways to create a database. The first one is to
        use the database instance as below:

            database = Database(path_or_url=path_to_file)

        The second one is by subclassing the Model class:

            class Celebrity(Model):
                pass

        If you decide to create the database inline, you need to provide
        the fields, model name [...] exactly like you would for subclassing
        the Model class.

    Parameters
    ----------

        path_or_url: is the path or the url of the schema/json that you wish to use

        fields: are the fields that you want to create if the database does not exist

        types: are the types of each fields

            This process can be facilitated by using the Fields classes such as
            IntegerField, CharField etc.
    """
    def __init__(self, path_or_url=None, **kwargs):
        self.path_or_url = path_or_url
        self.kwargs = kwargs

        if self.path_or_url:
            path_exists = os.path.exists(path_or_url)
            if not path_exists:
                pass
            else:
                db_data = self.load_database(path_or_url)

            self.db_name = os.path.basename(path_or_url)
            # Initializes the database data within
            # the Functions() class
            self.db_data = db_data['data']
            # Manager for interracting with the database
            self.manager = Manager(data=self.db_data)

    def create(self, name, fields:list, models:list=None, **kwargs):
        """A definition that can create a database outside of
        of a class based structure.

        Description
        -----------

            Suppose we want to create a new database and return the
            handle (cursor) of the latter. We can do so by using:

        Parameters
        ----------

            Fields: they can be either string values or Field classes that
            we be converted accordingly for the database
        """
        # if self.path_or_url:
        #     raise DatabaseError('You are trying to both load and create a database at the same time.' 
        #         ' If you wish to create a new database, do not use path_or_url')
        # print(name, fields, models)
        pass

    def migrate(self, **kwargs):
        """Creates a new version of the database by changing the
        modified_on and increasing the version of the schema
        """
        pass
    
    def pre_save(self, func=None):
        """A decorator that performs a set of actions before
        saving data to the database
        """
        return self.save(data=func(self.db_data))

    def post_save(self, func=None):
        """A decorator that performs a set of actions after
        saving data to the database

        Example
        -------

            @database.post_save
            def my_definition(data):
                if data:
                    if a in data:
                        data[a] = ''
                    return data
        """
        saved_data = self.save(data=func(self.db_data))
        return saved_data

    def pre_delete(self):
        pass

    def post_delete(self):
        pass

    @classmethod
    def save(cls, data=None, **kwargs):
        """A definition that commits changes to the database
        by writting objects into it
        """
        # If data is None, then
        # just return the cached_version
        # of the database to the user
        if data is None:
            return ''

        # If data is passed but is not a dict,
        # then directly raise an exception here
        if data and not isinstance(data, dict):
            raise Exception()
        else:
            # cls.clean(data=data)

            # Otherwise we can open the database in order
            # to commit the new changes
            with open(PATH, 'w', encoding='utf-8') as f:
                data['$modified_on'] = cls.set_date()
                json.dump(data , f, indent=4, sort_keys=True)
            return cls

    def load_database(self, path_or_url):
        """A simple function that opens the local database
        to retrieve all the data that it contains
        """
        with open(path_or_url, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return self.check_schema(data)

    def refresh_from_database(self):
        pass
    
    def check_kwargs(self, **kwargs):
        return kwargs

    def check_schema(self, data):
        """This function is called everytime the database is loaded in order
        to check for the integrity of the database we are going to work with.

        Description
        -----------

            It checks of the presence of the following fields:
                - iD
                - Created_on
                - Version

            The presence of certain fields can raise an error or not
        """
        if '$id' not in data:
            raise SchemaError('We could not find the required key $id in the schema of your database')
        else:
            # Here we create a valid identifier for the
            # the databaase if it is none or blank
            if data['$id'] is None or data['$id'] == '':
                data['$id'] = secrets.token_hex(nbytes=25)

        # Require a created_on date so that we
        # can also keep track of the version of
        # the database
        if '$created_on' not in data:
            data['$created_on'] = self.set_date()
        else:
            if data['$created_on'] == None or data['$created_on'] == '':
                data['$created_on'] = self.set_date()

        if '$version' not in data:
            data['$version'] = 0
        else:
            if data['$version'] == None or data['$version'] == '':
                data['$created_on'] = 0
        return data
    
    @staticmethod
    def set_date():
        """Get the current date as a timestamp"""
        return datetime.datetime.now().timestamp()

    @staticmethod
    def calculate_version(n):
        """Bump the current database version by one"""
        return n + 1

    def clean(self, **kwargs):
        """This definition is called just before data is committed (or written)
        to the database in order to prevent corruption.
        """
        pass
    
class Models(type):
    """Models are a way of structuring the logic of your database
    efficiently using class methods

    Description
    -----------

        class FashionModels(Models):
            pass
    """
    def __new__(cls, name, bases, cls_dict):
        new_class = super().__new__(cls, name, bases, cls_dict)
        if name != 'A':
            model_name = name
            fields_to_create = []
            # Get each fields from the database in order
            # to be able to create the model
            for key, value in cls_dict.items():
                if isinstance(value, CharField):
                    item = value.as_dict
                    item['name'] = key
                    fields_to_create.append(item)

                    # Use a database instance to create
                    # all the models
                    database = Database()
                    database.create(model_name, [], fields_to_create)
                    # Implement the instance to all models
                    setattr(new_class, 'database', database)
        return new_class

class A(metaclass=Models):
    def save(self, data=None):
        pass
