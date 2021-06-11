import requests
import urllib

def get_videos(published_after, keyword, APIKEY, next_page_token):
    base_url = 'https://youtube.googleapis.com/youtube/v3/search?'
    params = {
        'part': 'snippet',
        'maxResults': 50,
        'order': 'date',
        'publishedAfter': published_after,
        'q': keyword,
        'type': 'video',
        'key': APIKEY
    }
    if next_page_token:
        params['pageToken'] = next_page_token

    url = base_url + urllib.parse.urlencode(
        params, safe='+=/', quote_via=urllib.parse.quote
    )

    resp = requests.get(url)
    return resp
