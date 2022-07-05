import time
from functools import wraps

from django.db import connection, reset_queries


def query_debugger(func):

    @wraps(func)
    def inner_func(*args, **kwargs):
        """
        Counts time and number of queries for request.
        """

        reset_queries()

        start_queries = len(connection.queries)
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()
        end_queries = len(connection.queries)

        # Output
        print("-----------------------------")
        print(f"Function: {func.__name__}")
        print(f"Finished in: {(end - start):.2f}s")
        print(f"Number or queries: {end_queries - start_queries}")
        print("-----------------------------")

        return result
    return inner_func
