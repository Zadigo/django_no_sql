No-SQL Django database
======================

The nosql Django database is an application that allows anyone to implement a nosql Database in a Django or Flask application.

Organization
------------

The application is composed of 5 main important elements that we will describe below:

    - Database
    - Functions
    - Queryset
    - Fields
    - Managers

Database
--------

The database module is the main entrypoint for anything related to creating and managing your database at the top level.

## Using Database inline

You can create or open a database in multiple ways. The first, is the inline method.

```
from django_no_sql.db.database import Database

database = Database(path_or_url=path/to/database.json)
```

By utilizing this technique, you also need to provide fields and model name or your database would be just an empty file.

```
from django_no_sql.db.database import Database
from django_no_sql.db.fields import CharField, IntegerField

database = Database(path_or_url=path/to/database.json)

database.model_fields = [CharField(), IntegerField()]
database.field_names = [name, age]
```

On initialization, the Database class checks whether the JSON file exists and if it needs to create a new one.

**NOTE:** The database alway calls the __check\_schema()__ function on load.

## Using Models

Models are another way for creating your database by subclassing them. When the models are initialized, they automatically run a set of functions that make it very easy to delete fields or rename your models with ease.

```
from django_no_sql.db.models import Models

class Celebrity(Models):
    name = CharField(45)
    age = CharField(minimum=18)

    def __str__(self):
        return self.name
```

Functions
---------

The functions class __regroups all the required of logic used to translate expressions into something that can retrieve the data from the database based on criterion__.

For example, if we wanted to get all the records where the name matches Kendall, we would use one of the following expressions: `name=Kendall`, `name__eq=Kendall`, `name__contains=Kendall` or `name__exact=Kendall`.

You'll observe that expressions are exactly similar to what you would use in Django.

For example, lets say you have the following query parameter: `.get(name=kendall)`. Now, suppose you have the following data structure:

The Functions class will translate the expressions above into `[name], [Kendall]` or `[name], [Kendall], [eq]` by identifying and grouping each parts logically allowing for have complex structures such `.filter(location__country=USA)`

The Functions class is data-blind on start. In other words is does not know the existence of data until the `.db_data` global parameter has been initialized with the database data.

## The algorithms

The Functions class is composed of three main definitions:

    - Comparator
    - Iterator
    - Decomposer

The Iterator is responsible for __iterating over the data, the query expressions and the searched values__ at once. It returns the records in the database that correspond to the expressions used to filter them.

During iteration loop, __each expression is either decomposed or not__ depending on their level of complexity in order to match their criterion.

To do so, the logic functions in a way that __if the key and its value cannot be extracted naturally from a single database record, then we must be dealing with a complex expression__ (e.g. `location__country`). In such a case, decompose it: `[location, country]` so that we can get the exact value of the record to work with.

---

__NOTE:__ A __natural key__ is a key that we can retrieve without any complex process. For example, `name` or `location` in `{name: Kendall, location: {country: USA}}`.

`country` however, requires a special process in order to get its value. It is a __non-natural key__ (e.g. `location__country`).

---

Once the expressions have been decomposed, we can then confront the searched value with the database data using the expression parameter. For example, `name: Kendall` using `contains` against `{name: Kendall, surname: Jenner}`.

If the comparision is true, then we can return that record.

In the case of queries having multiple expressions e.g. `.get(name=Kendall, location__country=USA)`, the iteration is done twice. Once for `name: Kendall` and a second time for `location -> country: USA`.

The boolean result of the comparisions are appended in a list and smashed in a pure Python `all([true, true])` function in order to determine if each criteria was met.

If the outcome is true, we can return the record. This is the equivalent of using _AND_ in SQL.

# Managers

Managers allow you to interract with the data of your database by running queries for example.

Managers can work with two sorts of data: __naive data__ and __database instance__. Naive data is data that has no extended functionnalities and are not callable objects: `[{name: Kendall}]`.

On the other hand, database instances contains the data on which we can call additional functions such save, update etc. contained within their body or their super class. In other words, they can modify the data on the fly.

Models typically use database instances that would then allow you through the manager to update, save or delete records.

## Get

## Get Rand

## Get Or Create

## Filter

## All

## Include and Exclude

## Insert

## Delete

## Values

## Limit

## First

## Last

## Count


# Queries and Querysets

Queries and Querysets wrap the data that was retrieved from the database and implement additional functionnalities to them.

__NOTE:__ All objects returned by Functions from the database are dictionnary objects that can then be directly used in your templates.

## General

To query your database, you'll generally use the following strucure: `name=something`, `address__location=something` -; or with special keywords: `name__eq=something`, `age__gt=16`.

We will see these different keyword elements below.

## Query functions

### Get

When you wish to retrieve one item from your database, this is the function to use.

The function `.get()` returns a Query object.

### Filter

### Exlude & Include

## Special keywords

### Equals and not equals

### Greater than/Not greater than

## Operators

# Extended functionnalities

## Aggregates

Aggregates regroup a list of functions that allow you to aggregate data and return the output. The __Aggregate__ class is the main entrypoint for all other classes that perform aggregation.

### Sum

### STDev

### Avg

### WeightedAvg

### Count

### Variance

### Min and Max