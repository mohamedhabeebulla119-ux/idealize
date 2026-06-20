from backend.cache import cache_manager

def test_cache_set_and_get():
    # Clear memory cache for this test
    cache_manager.cache = {}
    
    # Generate a dummy entry
    prefix = "test"
    kwargs = {"query": "apple", "user": "admin"}
    value = {"result": "success"}
    
    # Verify it doesn't exist yet
    assert cache_manager.get(prefix, **kwargs) is None
    
    # Set the cache
    cache_manager.set(prefix, value, **kwargs)
    
    # Verify it exists now
    cached_value = cache_manager.get(prefix, **kwargs)
    assert cached_value == value
    
    # Verify a slightly different query returns None
    assert cache_manager.get(prefix, query="orange", user="admin") is None
