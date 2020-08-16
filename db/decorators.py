from django_no_sql.db import errors

def database_cache(func):
    """A cache function that stores the data coming from the
    database and returns a dictionnary.

    Result
    ------

        {schema: '', data: '', id: ''}
    
    Parameters
    ----------
        
        path: current path to the database
        
        key: the main key entrance to access the database data
    """
    pass

def database_cache_for_web(func):
    pass
