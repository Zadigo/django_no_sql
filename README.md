# No-SQL Django database

The nosql Django database is an application that allows anyone to implement a nosql Database in a Django or Flask application.

# Organization

The application is composed of x main important elements that we will describe below:

    - Database
    - Functions
    - Queryset

## Database

The database module is the main entrypoint for anything related to creating and opening your database.

For instance, opening a database is done as followed:

```
db = Database(path_or_url=path)
```

### Creating a database using Models

Models are the base element to use if you wish to create a database in a Django application.

```
from django_api.db.database import Models

class Celebrity(Models):
    name = CharField(45, blank=True, null=True)
    surname = CharField(45, blank=True, null=True)

    def __str__(self):
        return self.name
```

---

## Functions

The functions class regroups a set of logic used to translate a query parameter into something that can retrieve the data from the database.

For example, lets say you have the following query parameter: `.get(name=kendall)`. Now, suppose you have the following data structure:

```
    {
        data: {
            1: {
                name: Kendall
                surname: Jenner
                location: {
                    country: USA
                }
            }
        }
    }
```

The Functions class will translate the query parameter `[name], [Kendall]` to retrieve the the first object.

In that regards, we can have complex structures such `.filter(location__country=USA)` in the same way that you would do with Postgres or SQlite.

The Functions class is data-blind. In other words is does not know the existence of data until the `.db_data` global parameter has been initialized with the database data.

The Functions class is composed of three main definitions:

    - Comparator
    - Iterator
    - Decomposer

The Iterator is responsible for __iterating over the data, the query parameters and the searched values__ at once.

During phase, __each query parameter is either decomposed or not__ depending on their level of complexity.

To do so, the logic functions such as __if the key and its value cannot be naturally be extracted from data, then we must be dealing with a complex query__ (e.g. `location__country`). In such a case, decompose it/them: `[location, country]`.

---

__NOTE:__ A __natural key__ is a key that we can retrieve without any complex process. For example, `name` or `location` in `{name: Kendall, location: {country: USA}}`.

`country` however, requires a special process in order to get its value. It is a non-natural key (e.g. `location__country`).

---

Once the values have been decomposed, then we can compare the searched value with database data using the query parameter: `searched_value: Kendall` using `contains` against `{name: Kendall, surname: Jenner}`.

If the comparision is correct, then we can return that record.

In the case of queries having multiple parameters e.g. `.get(name=Kendall, location__country=USA)`,  the iteration is done twice.

Once for `name: Kendall` and a second time for `location -> country: USA`. The boolean result of the comparisions are appended in a list and an `all()` Python function is called on the latter.

If the outcome is true, we can return the record: e.g. `all([true, true])` would return true. This is the equivalent of using 'and' in SQL.

# Queries

Queries are a way for you to retrieve data from the database. As explained beforehand, these queries are translated by he Functions class.

__NOTE:__ All objects returned by the functions are dictionnary objects that can then be directly used in your templates.

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