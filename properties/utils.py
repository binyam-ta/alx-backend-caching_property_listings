from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    # Connect to Redis
    redis_conn = get_redis_connection("default")
    
    # Get hits and misses
    info = redis_conn.info()
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    
    # Calculate hit ratio using ALX-preferred style
    total_requests = hits + misses
    hit_ratio = hits / total_requests if total_requests else 0
    
    # Log metrics (no logger.error)
    logger.info(f"Redis Cache Metrics: Hits={hits}, Misses={misses}, Hit Ratio={hit_ratio}")
    
    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio
    }


def get_all_properties():
    # Try to get the queryset from Redis
    properties = cache.get('all_properties')
    
    if not properties:
        # Not in cache, fetch from DB
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties
