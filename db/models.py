from django_no_sql.db.database import Database
from django_no_sql.db.fields import Field
import inspect
from django_no_sql.db.managers import Manager
from django_no_sql.db.errors import NullFieldError

class BaseModel(type):
    """Models are a way of structuring the logic of your database
    efficiently using class methods

    Description
    -----------

        class FashionModels(Models):
            pass
    """
    def __new__(cls, name, bases, cls_dict):
        new_class = super().__new__(cls, name, bases, cls_dict)
        if name != 'Model':
            model_name = name
            model_fields = []
            fields_to_create = []
            # Get each fields from the database in order
            # to be able to create the model
            for key, field in cls_dict.items():
                if not key.startswith('__'):
                    if isinstance(cls_dict[key], Field):
                        item = field.as_dict
                        item['name'] = key
                        model_fields.append(field)
                        fields_to_create.append(item)

            # Use a database instance to create
            # all the models
            # database = Database()
            # database.model_name = model_name
            # database.model_fields = model_fields
            # database.create(model_name, fields_to_create)
            # Implement the instance to all models
            # setattr(new_class, 'database', database)
        return new_class

class Model(metaclass=BaseModel):
    def __init__(self):
        # We get the attributes of the model
        # in order to create a custom database
        # based on the data we received
        model_members = inspect.getmembers(self, lambda a: not(inspect.isroutine(a)))
        model_attributes = [model_member for model_member in model_members if not(model_member[0].startswith('__') and model_member[0].endswith('__'))]
        
        database = Database()
        database.model_name = self.__class__.__name__

        field_names = []
        model_fields = []

        for model_attribute in model_attributes:
            if model_attribute[0] == 'Meta':
                # Meta adds additional pieces of paramters
                # and informations to the database
                if isinstance(model_attribute[1], type):
                    allowed_attributes = ['abstract', 'plural', 'proxy']
                    meta_dict = model_attribute[1].__dict__
            else:
                # (name, CharField({...}))
                field_names.append(model_attribute[0])
                model_fields.append(model_attribute[1])

        database.field_names = field_names
        database.model_fields = self.check_fields(model_fields)
          
        # We can create the database here --;
        # each model would have their specific
        # model instance
        database.create_from_model(database.model_name, database.model_fields)

        self.database = database
        self.manager = Manager(db_instance=self.database)

    def check_fields(self, fields):
        """Checks whether the field is not None and
        is a subclass of Field"""
        none_fields = []
        for field in fields:
            if field is None:
                none_fields.append(field)
        
        if none_fields:
            raise TypeError('Field "%s" should not be None' % none_fields)
        
        return fields
