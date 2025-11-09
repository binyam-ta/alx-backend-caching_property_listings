from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

# Optional: you can keep page-level caching too
@cache_page(60 * 15)
def property_list(request):
    properties = get_all_properties()
    return JsonResponse(properties, safe=False)
