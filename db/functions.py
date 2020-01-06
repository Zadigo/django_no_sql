from collections import OrderedDict, namedtuple
from itertools import dropwhile, filterfalse, takewhile

from django_no_sql.db.errors import (FilterError, ItemExistError,
                                     KeyExistError, SubDictError)


class Functions:
    """This class regroups all the given logic in order transform filters
    into usable pieces of logic for filtering data withing your database.
    """
    db_data = dict()
    special_words = ['eq', 'gt', 'gte', 'lt', 'lte', 
                        'ne', 'contains', 'icontains', 'exact', 'iexact']
    # A list that holds
    # all the filter keys
    keys_dict = []
    # A list that holds
    # all the values the
    # user wants to filter
    # against
    searched_values = []

    @property
    def last_item_id(self):
        """Get the last items' iD in the data
        """
        return int(list(self.db_data.keys())[-1])

    @property
    def auto_increment_last_id(self):
        return self.last_item_id + 1

    def transform_data(self, data:dict=None):
        """Transforms the data from the database into an array
        containing a series of dictionnaries.

        Example
        -------

            {1: {a: b, c: d}
            
            By transforming the data, we can obtain the following:

                [{a: b}, {c: d}]
        """ 
        return [single_item for single_item in self.db_data.values()]

    def simple_decompose(self, key):
        """A simple defintion that separates a query in a list

        Result
        ------

            If we have location__country then we can get:

                [location, country]
        """
        if '__' in key:
            keys = key.split('__')
        else:
            # If there's nothing, just
            # return the key as is - wrap the key
            # in a list to allow iteration
            return [key]
        return keys
    
    def decompose(self, **query):
        """Decomposes a query from its parameters

        Description
        -----------

            Queries are dictionnaries composed of their keys and parameters:

                {name: Kendall, location__country: USA}
            
            By decomposing the dict, we get two separate arrays, one containing
            only the keys, the other, only the searched values:

                [name, location__country]

                [Kendall, USA]

        Parameters
        ----------

            query: is the keyword arguments

        Result
        ------

            decompose() returns the length of the keys_dict
        """
        # Now we can seperate the keys from
        # the search values so that we have
        # two independent arrays from one another
        for key, value in query.items():
            self.keys_dict.append(key)

            # NEW: In certain situations, the value
            # can be an operator (e.g. F, When, OR...)
            # In that specific case, we need to call the
            # corresponding function of that operator which
            # would then return the value that we want to filter
            # from a set of records

            self.searched_values.append(value)
        return len(self.keys_dict)

    def available_keys(self, check_key=None):
        """Returns the list of available keys that can
        be used to query the data

        Parameters
        ----------

            check_key: pass a string to check if something
            is present in the available keys        
        """
        if self.db_data is None:
            return []
        # We can come from the premise
        # that all the keys are structured
        # the exact same manner -- in which
        # case, by taking on sample from the
        # data that we want to query, we can
        # get the general keys' structure 
        # of all the rest of the data
        keys = [key for key in self.db_data.keys()]

        if check_key:
            if check_key in keys:
                return True
            else:
                return False

        # Now get the available keys
        # from the sample dict
        return keys

    def right_hand_filter(self, f, sub_dict):
        """A special function that takes the extended
        base filter in order to transform them into a logic
        that can filter the data from the database

        Description
        -----------

            {location: {country: USA}}

            Suppose we have 'location__country' as a filter to
            get USA in the dict above. In which case, the definition
            will split the paramaters to get the specific value.

        Parameters
        ----------

            f: a filter such as something__a or something__a__b

            sub_dict: a subdictionnary that we want to filter

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

        # We also know that the final filter
        # (if there is one), can be a special
        # keyword that we need to do something with
        splitted_values = f.split('__', 5)
        number_of_keys = len(splitted_values)

        # We iterate over each keyword
        # using the index. At each iteration,
        # we get +1 depth into the dict we
        # are trying to filter
        for i in range(0, number_of_keys):
            key = splitted_values[i]
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
                        raise KeyExistError(key, self.available_keys())
                except KeyError:
                    # If the key is not present,
                    # we can raise an error here
                    if key not in self.special_words:
                        print('Available keys are: %s' % self.available_keys())
                        raise
            else:
                # Pass the special keyword
                # filter for the comparator
                # that we will be calling below
                special_keyword = key
        # If everything went well,
        # we should have got the
        # value that we were looking for and
        # return with that the special keyword
        return sub_dict_copy, special_keyword

    def comparator(self, a, b, special_keyword='exact'):
        """A definition used to compare two given values
        and returns True or False.

        Parameters:

            a: the reference value to compare

            b: the value the user wants to compare to a

            special_keyword: the filter word to use to make the comparision

            By default, we always search for the exact value
        """
        if special_keyword not in self.special_words:
            raise FilterError('The filter that you used is not implemented in the Functions class', special_keyword)

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

    def iterator(self, data=None, **query):
        """This definition iterates over each dict from the data
        that we wish to filter and then triggers a logic in order
        to extract each element accordingly.

        Description
        -----------

            The iterator iterates by default over all the data of the
            database.

        Parameters
        ----------

            query: is the filter that we wish to apply. For example name__contains
            or location__country=USA

        Result
        ------

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

            And would be wrapped in the QuerySet class
        """
        special_word = 'exact'
        number_of_filters = self.decompose(**query)

        comparator_results = []
        filtered_items = []
        number_of_values_to_search = len(self.searched_values)
        position = 0

        # By default, we query on all
        # the data present in the database
        # if data is None
        if data is None:
            data = self.transform_data()

        # This section iterates over both
        # arrays in order to filter the data
        for item in data:
            for key in self.keys_dict:
                searched_value = self.searched_values[position]
                try:
                    no_underscore = item[key]
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
                        raise  SubDictError(key, item[key])
                except KeyError:
                    no_underscore = None
                    # If the key contains a double
                    # underscore we need to separate
                    # the key from the special keyword
                    result = self.right_hand_filter(key, item)
                    with_underscore = result[0]
                    special_word = result[1]

                # Here we can get the parameter
                # that resulted into a true
                g = no_underscore or with_underscore

                if number_of_filters == 1:
                    # This logic is specific to cases where
                    # we only have one filter
                    return_value = self.comparator(g, searched_value, special_keyword=special_word)
                    if return_value is True:
                        filtered_items.append(item)
                elif number_of_filters > 1:
                    # This logic works for cases where we have
                    # multiple filters. It's like applying an AND
                    # operator in an SQL statement.

                    # The logic is to get all the booleans in an array
                    # and to apply an all() function that will determine
                    # if the item needs to be appended or not
                    comparator_results.append(self.comparator(g, searched_value, special_keyword=special_word))

                position = position + 1
                # In order for the cursor to always iterate
                # between the 0 and the max amount of values
                # that the user wants to search, we have to reset it
                if position >= number_of_values_to_search:
                    position = 0

            # This is the section with the all() function that
            # determines if everythong is TRUE in order to append
            # the item in the array or not
            if number_of_filters > 1 and all(comparator_results):
                filtered_items.append(item)
        return filtered_items

    def get_by_id(self, reference_or_id:int):
        """Return an item from the database that corresponds exactly
        to the given id.
        
        Description
        -----------

        This special function was created in order to
        prevent useless iteration over the datbase.
        """
        try:
            item = self.db_data[str(reference_or_id)]
        except:
            raise ItemExistError(reference_or_id)
        else:
            return item

    def filter_by_ids(self, ids:list):
        """From a list of ids, return a list of items that
        corresponds to the given ids
        """
        data = self.db_data['data'].keys()
        for all_id in all_ids:
            for element_id in ids:
                if all_id == element_id:
                    yield self.db_data[element_id]
