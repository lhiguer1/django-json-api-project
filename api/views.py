from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from requests import get
from django.core.cache import cache

BREAKING_BAD_API_BASE_URL = 'https://www.breakingbadapi.com/api/'

# Create your views here.
def ping(request: WSGIRequest):
    return JsonResponse({'success': True}, status=200)

def get_characters_from_api(name) -> list:
    key = ''.join(name.split()) # all whitespace

    characters = cache.get(key)
    if not characters:
        resp = get(BREAKING_BAD_API_BASE_URL+'characters', params={'name': name})
        characters = resp.json()
        cache.set(key, characters, timeout=60*5)
    return characters # list of characters

def parse_names(names_string:str):
    return list({name.strip().lower() for name in names_string.split(',') if name})

def characters(request: WSGIRequest):
    names_query = request.GET.get('names')
    if not names_query:
        return JsonResponse({'error': "names parameter is required"}, status=400)

    names = parse_names(names_query)

    all_characters = {}
    for name in names:
        results = get_characters_from_api(name)
        all_characters |= { # set union ops works with dict
            character['char_id']:character for character in results
            if character['char_id'] not in results
            } 
    
    return JsonResponse(sorted(all_characters.values(), key=lambda x: x['char_id']), status=200, safe=False)
    