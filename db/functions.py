import copy
import datetime
import re
from collections import OrderedDict

from django_no_sql.db import errors
from django_no_sql.db.errors import FilterError, ResolutionError, SubDictError


class Functions:
    """
    This is the main class that implements all the logic for
    querying and comparision of data in the database
    """
    db_data = []
    new_queryset = []

    special_words = ['eq', 'gt', 'gte', 'lt', 'lte', 'startswith', 'endswith',
                        'ne', 'contains', 'icontains', 'exact', 'iexact', 're']

    special_date_keywords = ['year', 'day', 'month']

    # A list that holds
    # all the filter keys
    keys_dict = []
    # A list that holds
    # all the values the
    # user wants to filter
    # against
    searched_values = []

    @property
    def has_new_queryset(self):
        """Checks the new queryset property is populated"""
        return True if self.new_queryset else False

    @property
    def has_queryset(self):
        """Checks whether the instance has a queryset new or not"""
        return any([self.new_queryset, self.db_data])

    def iterator(self, query=None, **expressions):
        """
        This definition iterates over each record that
        we wish to filter and then triggers a logic in order
        to extract items accordingly

        Description
        -----------

            The iterator iterates by default over all the data of the
            database

        Parameters
        ----------

            query (str, optionnal): is an optionnal queryset on which we want to run expressions

            expressions (str, optionnal): are the filters that we wish to apply. 
                        For example name__contains or location__country=USA

        Returns
        -------

            list: of the records that were filtered

            Suppose we have the following data with the constraint that name should be Kendall:

                [
                    {
                        name: Kendall,
                        location: {
                            country: USA,
                            city: Florida
                        }
                    },
                    {
                        name: Hailey,
                        location: {
                            country: USA,
                            city: Florida
                        }
                    }
                ]

            The final result would be:

                [
                    {
                        name: Kendall,
                        location: {
                            country: USA,
                            city: Florida
                        }
                    }
                ]
        """
        special_keyword = 'exact'
        number_of_filters = self.decompose(get_count=True, **expressions)

        comparator_results = []
        filtered_items = []
        # number_of_values_to_search = len(self.searched_values)
        # position = 0

        items_to_iterate = self.new_queryset or self.db_data
        # if self.new_queryset:
        #     items_to_iterate = self.new_queryset
        # elif not self.new_queryset and self.db_data:
        #     items_to_iterate = self.db_data
        
        if query is not None:
            items_to_iterate = query

        if not items_to_iterate:
            return []

        if not isinstance(items_to_iterate, list):
            raise errors.QueryTypeError(query)

        # This section iterates over both
        # arrays in order to filter the data
        for item in items_to_iterate:
            for index, key in enumerate(self.keys_dict):
                searched_value = self.searched_values[index]

                try:
                    no_underscore = item[key]

                    # We need to reset the special keyword
                    # to the default value which is eq or exact
                    special_keyword = 'exact'
                    # There are cases where we might not have reached
                    # the full depth of a subdictionnary.

                    # For example suppopse we have this:
                    # {a: b, c: {d: e}} and the user queries
                    # .get(c=something). In such a case, we
                    # can see that the user did not query a
                    # a specific key from the subdict (c).

                    # This results in the return value
                    # being a subdict.

                    # Therefore, we just append the
                    # subdict into the filtered items(?)
                    # or raise an error telling the user
                    # that the subdict needs to be queried(?)
                    if isinstance(no_underscore, dict):
                        # filtered_items.append(item[key])
                        raise errors.SubDictError(key, item[key])
                except KeyError:
                    no_underscore = None
                    # If the key contains a double
                    # underscore we need to separate
                    # the key from the special keyword
                    result = self.right_hand_filter(key, item)
                    with_underscore = result[0]
                    special_keyword = result[1]

                # Here we can get the parameter
                # that resulted into a true
                g = no_underscore or with_underscore

                if number_of_filters == 1:
                    # This logic is specific to cases where
                    # we only have one filter
                    return_value = self.comparator(g, searched_value, special_keyword=special_keyword, sub_dict=item)
                    if return_value is True:
                        filtered_items.append(item)
                elif number_of_filters > 1:
                    # This logic works for cases where we have
                    # multiple filters. It's like applying an AND
                    # operator in an SQL statement.

                    # The logic is to get all the booleans in an array
                    # and to apply an all() function that will determine
                    # if the item needs to be appended or not
                    comparator_results.append(self.comparator(g, searched_value, special_keyword=special_keyword))

                # position = position + 1
                # # In order for the cursor to always iterate
                # # between the 0 and the max amount of values
                # # that the user wants to search, we have to reset it
                # if position >= number_of_values_to_search:
                #     position = 0


            # This is the section with the all() function that
            # determines if everything is TRUE in order to append
            # the item in the array or not
            if number_of_filters > 1 and all(comparator_results):
                filtered_items.append(item)
            # We need to reset the comparator results
            # variable in order to prevent it from 
            # appending all the thruth/false values
            # of all the tested data
            comparator_results = []
        self.new_queryset = filtered_items
        return filtered_items

    def decompose(self, get_count=False, **expressions):
        """A more complex query expression separator that can
        also separate logical comparision keywords e.g. gt, lt
        and also separate multiple query expressions

        Description
        -----------

            Queries are dictionnaries composed of their keys and parameters:

                { name: Kendall, location__country: USA }
            
            By decomposing the dict, we get two separate arrays, one containing
            only the keys, the other, only the searched values:

                [name, location__country]

                [Kendall, USA]

        Parameters
        ----------

            expressions: is the keyword arguments used to launch the search

        Result
        ------

            { name: Kendall, location__country: USA }
                becomes [[name, location__country], [Kendall, USA]]
            
        """
        # Now we can seperate the keys from
        # the search values so that we have
        # two independent arrays from one another
        for key, value in expressions.items():
            self.keys_dict.append(key)

            # NEW: In certain situations, the value
            # can be an operator (e.g. F, When, OR...)
            # In that specific case, we need to call the
            # corresponding function of that operator which
            # would then return the value that we want to filter
            # from a set of records

            self.searched_values.append(value)
        if get_count:
            return len(self.keys_dict)
        return [list(self.keys_dict), list(self.searched_values)]

    def number_of_queries(self):
        return

    def simple_decompose(self, expression):
        """A definition that separates a string type query 
        expressions into a list containing the keywords

        Example
        ------

            location__country becomes [location, country]
        """
        if '__' in expression:
            expressions = expression.split('__')
        else:
            # If there's nothing, just
            # return the key as is - wrap the key
            # in a list to allow iteration
            return [expression]
        return expressions
    
    def comparator(self, a, b, special_keyword='exact', sub_dict:dict=None):
        """A definition used to compare two given values
        and returns True or False.

        Parameters:

            a: the reference value to compare

            b: the value the user wants to compare to a

            special_keyword: the filter word to use to make the comparision

            Sub_dict: It corresponds to the sub dictionnary to use for functions
            resolution ex. F, Q...

            By default, we always search for the exact value
        """
        # FIXME: If the searched value is an F function,
        # we have to resolve it and then pass the returned
        # value as the searched value for comparision
        if isinstance(b, F):
            b.resolve(data=[sub_dict])
            if len(b) == 1:
                if b.operations_on_fields:
                    b.operations_on_fields[0]
                else:
                    raise Exception()
        
        # Intercept regex keyword
        # for filtering
        if special_keyword == 're':
            get_match = re.match(b, a)
            if get_match:
                return True
            else:
                return False
                    
        # Intercept keywords that attempt to filter
        # date elements: year, day, month, week...
        # if special_keyword in self.special_date_keywords:
        #     try:
        #         # NOTE: For this to work, the initial date must follow
        #         # the english format convention: year-month-day
        #         date_to_compare = datetime.datetime.strptime(a, '%Y-%m-%d')
        #     except Exception:
        #         # The value to use is not a date or
        #         # might not be a date. In which case,
        #         # just return False as a soft escape
        #         # error
        #         return False
        #     else:
        #         if special_keyword == 'year':
        #             return date_to_compare.year == b

        # BUG: It happens that the special
        # keyword is set to None when a function
        # call this definition. This raises an error...

        # if special_keyword not in self.special_words:
        #     raise FilterError('The filter that you used is not implemented in the Functions class', special_keyword)
        
        # We then have to be sure that if special_keyword
        # is really None, to use the fallback "exact"
        # comparision in order to keep the flow
        if special_keyword is None:
            return a == b
         
        if special_keyword == 'exact' or special_keyword == 'eq':
            return a == b

        if special_keyword == 'gt':
            return a > b

        if special_keyword == 'gte':
            return a >= b

        if special_keyword == 'lt':
            return a < b

        if special_keyword == 'lte':
            return a <= b

        if special_keyword == 'ne':
            return a != b

        if special_keyword == 'contains':
            return b in a

        if special_keyword == 'startswith':
            return a.startswith(b)

        if special_keyword == 'endswith':
            return a.endswith(b)

    def right_hand_filter(self, expression, sub_dict):
        """A special function that takes expressions
        in order to transform them into a logic
        that can filter the data from the database

        Description
        -----------

            {location: {country: USA}}

            Suppose we have 'location__country' as an expression to
            get USA in the dict above. In which case, the definition
            will split the paramaters to get the specific value.

        Parameters
        ----------

            expression (str): An expression such as something__a or something__a__b

            sub_dict (dict): a subdictionnary of a database top dictionnary
            that we want to filter

        Result
        ------

            Returns the value that we were looking for and the special keyword
            as a tuple. For example:

                {name: Kendall} with a filter such as name__eq=Kendall

                Will give the following result:

                    (Kendall, eq)

                This tuple can then be used to compare the retrieved value and the
                searched one using the special keyword
        """
        # Use a copy of the subdict in order
        # to keep the original values just
        # in case we need to do something else
        sub_dict_copy = sub_dict.copy()

        special_keyword = None
        # We split the filters up to depth
        # of five so that we can query the
        # dictionnary as deep as the user wants

        # We also know that the final expression
        # (if there is one), can be a special
        # keyword that we need to do something with
        splitted_values = expression.split('__', 5)

        # We iterate over each keyword
        # using the index. At each iteration,
        # we get +1 depth into the dict we
        # are trying to filter
        for key in splitted_values:
            if key not in self.special_words:
                # We know that it is a 
                # dictionnary key to use in
                # order to get into subdicts
                try:
                    # If the subdict is a dict or is still
                    # a dict then we can keep going +1 in depth
                    if isinstance(sub_dict_copy, dict):
                        sub_dict_copy = sub_dict_copy[key]
                    else:
                        # Otherwise, there's nothing to
                        # query anymore and we can raise an
                        # error since the additional depth
                        # does not exist
                        raise errors.KeyExistError(key, self.available_keys())
                except KeyError:
                    if key not in self.special_words:
                        print(f'Available keys are: {self.available_keys()}')
                        raise
            else:
                # Pass the key to the special_keyword variable
                # that we will be using for the comparator below
                special_keyword = key
        # If everything went well,
        # we should have got the
        # value that we were looking for and
        # combined with the special keyword
        # as a tuple
        return sub_dict_copy, special_keyword

    def available_keys(self, check_key=None):
        """Returns the list of available keys that can
        be used to query the data

        Parameters
        ----------

            check_key (str, optionnal): pass a string to check if something
            is present in the available keys        
        """
        if self.db_data is None:
            return []

        db_data = self.db_data
        
        # db_data can be a list which can
        # generate an error. In which case,
        # try to obtain the first dict
        if isinstance(db_data, list):
            try:
                db_data = db_data[0]
            except:
                return []
        # We can come from the premise
        # that all the keys are structured
        # in the exact same manner -- in which
        # case, by taking one sample from the
        # data that we want to query, we can
        # get the general keys' structure 
        # of all the rest of the data
        keys = [key for key in db_data.keys()]

        if check_key:
            if check_key in keys:
                return True
            else:
                return False
        return keys

    def last_id(self, increment=False):
        """Returns the last iD of a queryset
        
        Parameter
        ---------
        
            Increment: Add one to the last iD"""
        return len(self.new_queryset) if self.has_new_queryset \
                        else len(self.db_data)

    def simple_expressions(self, *expressions):
        """Separates simple expressions
        
        Returns
        -------
        
            list: query=value becomes [query, value]
        """
        decomposed_expressions = []
        for expression in expressions:
            decomposed_expressions.append(expression.split('=', 1))
        return decomposed_expressions

    def reset_new_queryset(self):
        """Resets the new_queryset"""
        # .. database.manager.get(...)
        # .. database.manager.get(...)
        # In this situation, the second
        # query keeps in memory the new_queryset
        # of the previous query. This method
        # can be used to reset the new_queryset
        # from scratch and prevent this
        if self.has_new_queryset:
            self.new_queryset = []
            return True
        return False

    def get_by_id(self, reference_or_id:int):
        """Return an item from the database that corresponds exactly
        to the given id.
        
        Description
        -----------

            This special function was created in order to
            prevent useless iteration over the database.
        """
        try:
            item = self.db_data[reference_or_id]
        except:
            raise errors.ItemExistError()
        else:
            return item

    def filter_by_ids(self, ids:list):
        """From a list of ids, return a list of items that
        corresponds to the given ids
        """
        def iterate():
            for i in ids:
                for index, value in enumerate(self.db_data):
                    if i == index:
                        yield value
        return list(iterate())

    def copy(self):
        return copy.copy(self)

class F:
    """The F function resolves expressions for other function 
    classes such as Avg, Sum etc

    Description
    -----------

        It has a standalone query resolver that returns either a
        specific value or a list of values after the field has
        been resolved.

        The F function is extremely useful for doing equality,
        comparisions for example directly on a value or list of values.

        In other words, the F function represents the value in itself
        on which we can directly do comparisions.

    Example
    -------

        Let's say we have F(age) where age is equals
        to 24. We can do F(age) != 26 or F(age) == 25 -; or, if
        age is a list it returns a list of booleans.

    Parameters
    ----------

        Field (str): is a field that we which to resolve in a database value
        or list of values

    """
    functions = Functions()
    sign = 'eq'

    def __init__(self, field):
        self.field = field
        self.resolved_values = []
        self.operations_on_fields = []

    def resolve(self, data:list=None, for_save=False):
        """A function into which the database data can be passed
        in order for the function to operate.

        The resolve() definition result is dependent on the values that
        are passed to be resolved. For example, if a single value is passed, 
        then only only a single resolved value would be return.

        Parameters
        ----------

            data: the data that contains the dictionnaries on which
            we want to perform operations
        """
        try:
            copy_data = data.copy()
        except:
            print('Resolve was called without no data to resolve.')
            return []

        # self.functions.db_data = data

        # BUG: If self.field is None, we need to raise
        # a specific error on that part otherwhise
        # simple_decompose tries to find __ in None
        # and raises and error
        # if not self.field is None:
        #     pass

        for item in copy_data:
            keys = self.functions.simple_decompose(self.field)
            for key in keys:
                try:
                    item = item[key]
                except errors.KeyExistError:
                    print(self.functions.available_keys())
                    raise
            self.resolved_values.append(item)

            # If the modified value is directly for saving
            # into the database, then we prepare the sequence
            # if for_save:
            #     pass

        return self.resolved_values

    def __str__(self):
        # return str(self.resolved_values)
        return str(self.__class__)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.field})'
    
    def __eq__(self, value):
        return [resolved_value == value for resolved_value in self.resolved_values]

    def __ne__(self, value):
        return [resolved_value != value for resolved_value in self.resolved_values]

    def __gt__(self, value):
        return [resolved_value > value for resolved_value in self.resolved_values]
    
    def __lt__(self, value):
        return [resolved_value < value for resolved_value in self.resolved_values]

    def __mul__(self, a):
        if isinstance(a, F):
            # BUG: When we get an F function and if the
            # return values are two arrays of different
            # sizes, we need to do something to prevent
            # Python from raising an error

            return self.resolved_values + a.resolved_values
        return [value + a for value in self.resolved_values]

    def __sub__(self, a):
        if isinstance(a, F):
            # __sub__ is evaluated before
            # .resolve() by Python. We have
            # to find a way to inverse that
            # so that __sub__ works with the
            # data instead of None
            pass

    def __add__(self, a):
        """Addition of two F functions or an F function with an integer..."""
        if isinstance(a, F):
            # BUG: When we get an F function and if the
            # return values are two arrays of different
            # sizes, we need to do something to prevent
            # Python from raising an error

            return self.resolved_values + a.resolved_values
        return [value + a for value in self.resolved_values]

    def __len__(self):
        return len(self.resolved_values)


class Case:
    def __init__(self, *cases, default=None):
        self.cases = list(cases)
        self.name = None

    def __call__(self, queryset):
        return self.resolve(queryset=queryset)

    # def __repr__(self):
    #     return f'<{self.__class__.__name__} {self}>'

    def resolve(self, queryset=None):
        resolved_conditions = []
        for case in self.cases:
            result = case(queryset=queryset)
            if result:
                resolved_conditions.append(result)
        return resolved_conditions


class When(Functions):
    resolved_queryset = OrderedDict()

    def __init__(self, condition=None, then=None, default=None, **expressions):
        self.expressions = expressions
        self.then = then
        self.default = default

    def __call__(self, db_instance=None, queryset=None):
        # We have to pass an instance of the
        # queryset 
        query = db_instance or queryset
        records = self.iterator(query=query, **self.expressions)
        return self.resolve(queryset=records)

    # def __repr__(self):
    #     return f'<{self.__class__.__name__} {self}>'

    def resolve(self, queryset=None):
        new_records = []
        for record in queryset:
            for key, _ in record.items():
                record['age'] = self.then
            new_records.append(record)
        # return self.resolved_queryset
        return new_records
