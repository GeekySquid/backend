# app/core/cache.py
import json
from typing import Optional, Any
from datetime import datetime, timedelta
from app.core.logging import logger

class SimpleCache:
    """Simple in-memory cache (replace with Redis in production)"""
    
    def __init__(self):
        self._cache = {}
        self._expiry = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self._cache:
            # Check if expired
            if key in self._expiry and datetime.now() > self._expiry[key]:
                self.delete(key)
                logger.info(f"Cache expired for key: {key}")
                return None
            
            logger.info(f"Cache hit for key: {key}")
            return self._cache[key]
        
        logger.info(f"Cache miss for key: {key}")
        return None
    
    def set(self, key: str, value: Any, ttl: int = 600):
        """Set value in cache with TTL in seconds"""
        self._cache[key] = value
        self._expiry[key] = datetime.now() + timedelta(seconds=ttl)
        logger.info(f"Cache set for key: {key}, TTL: {ttl}s")
    
    def delete(self, key: str):
        """Delete value from cache"""
        if key in self._cache:
            del self._cache[key]
        if key in self._expiry:
            del self._expiry[key]
        logger.info(f"Cache deleted for key: {key}")
    
    def clear(self):
        """Clear all cache"""
        self._cache.clear()
        self._expiry.clear()
        logger.info("Cache cleared")
    
    def size(self) -> int:
        """Get cache size"""
        return len(self._cache)


# Global cache instance
cache = SimpleCache()
