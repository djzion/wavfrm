from time import time
from functools import wraps

def timed(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time()
        result = f(*args, **kwds)
        elapsed = time() - start
        print "%s took %s time to finish" % (f.__name__, elapsed)
        return result
    return wrapper