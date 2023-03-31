from myfunctions import execute_this
from CacheManager import CacheManager

cached_responses = CacheManager()

@execute_this
def test():
    print(cached_responses(a="help"))
    print(cached_responses())
