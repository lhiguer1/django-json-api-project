from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.core.cache import cache
import sys
import asyncio
import aiohttp

# known bug with eventloop
# https://github.com/aio-libs/aiohttp/issues/4324
if sys.platform == 'win32' or sys.platform == 'cygwin':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

BREAKING_BAD_API_BASE_URL = 'https://www.breakingbadapi.com/api/'

# Create your views here.
def ping(request: WSGIRequest):
    return JsonResponse({'success': True}, status=200)

async def fetch(session, name) -> list:
    key = ''.join(name.split()) # all whitespace

    characters = cache.get(key)
    if characters:
        return characters

    async with session.get(BREAKING_BAD_API_BASE_URL+'characters', params={'name': name}) as resp:
        characters = await resp.json()
        cache.set(key, characters, timeout=60*5*0)


    return characters # list of characters

async def fetch_all(names, all_characters):
    async with aiohttp.ClientSession() as session:
        for name in names:
            characters = await fetch(session, name)
            all_characters |= { # set union ops works with dict
                character['char_id']:character for character in characters
                if character['char_id'] not in all_characters
                } 

def parse_names(names_string:str):
    return list({name.strip().lower() for name in names_string.split(',') if name})

def characters(request: WSGIRequest):
    names_query = request.GET.get('names')
    if not names_query:
        return JsonResponse({'error': "names parameter is required"}, status=400)

    names = parse_names(names_query)

    all_characters = {}
    asyncio.run(fetch_all(names, all_characters))


    return JsonResponse(sorted(all_characters.values(), key=lambda x: x['char_id']), status=200, safe=False)
    