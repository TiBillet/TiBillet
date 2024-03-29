import base64

import requests, json, os
APIKEY = os.environ.get('API_PEXELS')

def random_url_photo(query=None):
    if query == None:
        query = "music"

    headers = {'Authorization': APIKEY}
    url = f'https://api.pexels.com/v1/search?query={query}&per_page=40&orientation=landscape&size=small'
    photos = []
    res = requests.get(f"{url}", headers=headers).json()
    for photo in res.get('photos') :
        photos.append(photo.get('src').get('original'))

    return photos



def b64encode(string):
    return base64.urlsafe_b64encode(string.encode('utf-8')).decode('utf-8')

def b64decode(string):
    return base64.urlsafe_b64decode(string).decode('utf-8')
