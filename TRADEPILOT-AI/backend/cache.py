import json
import os
import hashlib
from typing import Any, Dict

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'cache.json')

class CacheManager:
    """
    A simple persistent JSON file cache.
    Generates a deterministic hash based on route prefixes and kwargs.
    """
    def __init__(self):
        self.cache_file = CACHE_FILE
        self.cache: Dict[str, Any] = {}
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
            except Exception as e:
                print(f"[CacheManager] Failed to load cache: {e}")
                self.cache = {}
        else:
            self.cache = {}

    def _save_cache(self):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"[CacheManager] Failed to save cache: {e}")

    def _generate_key(self, prefix: str, **kwargs) -> str:
        # Create a stable string representation
        stable_str = json.dumps(kwargs, sort_keys=True)
        hash_val = hashlib.md5(stable_str.encode()).hexdigest()
        return f"{prefix}_{hash_val}"

    def get(self, prefix: str, **kwargs) -> Any:
        key = self._generate_key(prefix, **kwargs)
        if key in self.cache:
            print(f"[CacheManager] HIT -> {prefix}")
            return self.cache[key]
        return None

    def set(self, prefix: str, value: Any, **kwargs):
        key = self._generate_key(prefix, **kwargs)
        self.cache[key] = value
        self._save_cache()
        print(f"[CacheManager] SET -> {prefix}")

cache_manager = CacheManager()
