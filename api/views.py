from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from requests import get

BREAKING_BAD_API_BASE_URL = 'https://www.breakingbadapi.com/api/'

# Create your views here.
def ping(request: WSGIRequest):
    return JsonResponse({'success': True}, status=200)

def get_characters_from_api(name) -> list:
    resp = get(BREAKING_BAD_API_BASE_URL+'characters', params={'name': name})
    return resp.json() # list of characters

def parse_names(names_string):
    return list({name.strip() for name in names_string.split(',') if name})

def characters(request: WSGIRequest):
    names = parse_names(request.GET.get('names'))

    all_characters = {}
    for name in names:
        results = get_characters_from_api(name)
        all_characters |= {
            character['char_id']:character for character in results
            if character['char_id'] not in results
            } 
    
    return JsonResponse(sorted(all_characters.values(), key=lambda x: x['char_id']), status=200, safe=False)
    