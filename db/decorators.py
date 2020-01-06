def database_cache(func):
    def cached_data(self, path_or_url):
        """Opens the database and returns a cached version
        of the data that it contains
        """
        cached_data = func(self, path_or_url)
        return cached_data
    return cached_data