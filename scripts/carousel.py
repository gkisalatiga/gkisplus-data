from datetime import datetime as dt
from urllib.parse import urlparse, parse_qs
from zipfile import ZipFile as zf
import json
import os
import requests as rq
import time

s = rq.Session()

# The YouTube v3 API key.
print('Retrieving the API KEY secrets ...')
api_key = os.environ['YT_API_KEY']

def get_cleansed_video_id(yt_url):
    '''
    Obtain the video ID from a given YouTube URL.
    SOURCE: https://stackoverflow.com/a/39841923
    :param yt_url: the YouTube URL.
    '''
    parsed_url = urlparse(yt_url)
    return parse_qs(parsed_url.query)['v'][0]

def get_yt_snippet(video_id):
    '''
    Using YouTube API v3, retrieve a given video_id's video snippet information.
    :param video_id: the video ID of the YouTube video, without "http", "www", etc. in its string
    '''
    # The Google API bridge.
    bridge = 'https://www.googleapis.com/youtube/v3/videos'
    
    # Obtaining the video data.
    part = 'snippet'
    r = rq.get(bridge + f'?key={api_key}&part={part}&id={video_id}')
    
    # Do about the returned JSON data.
    j = r.json()
    j_snippet = j['items'][0]['snippet']
    
    # Determine if it is a live video.
    is_live = 0
    if j_snippet['liveBroadcastContent'] == 'live':
        is_live = 1
    
    # Prepare the return dict.
    a = {
        'yt-title': j_snippet['title'],
        'yt-date': j_snippet['publishedAt'].split('T')[0],
        'yt-desc': j_snippet['description'],
        'yt-link': f'https://www.youtube.com/watch?v={video_id}',
        'yt-thumbnail': j_snippet['thumbnails']['high']['url'],
        'yt-is_live': is_live
    }
    
    # Returning the result.
    return a

def execute():
    # Preamble logging.
    print('Beginning the automation script for initializing the carousel banners ...')
    t = dt.now()
    
    # Overwriting the zip archive file.
    # SOURCE: https://docs.python.org/3/library/zipfile.html
    print('Creating the ZIP archive and compressing ...')
    with zf('gkisplus-carousel.zip', mode='w', compression=8) as fo:
        
        # Recurse into the static folder.
        # SOURCE: https://docs.python.org/3/library/os.html
        for a, b, c in os.walk('carousel'):
            for l in c:
                print(f'Adding file to the ZIP archive: {os.path.join(a, l)} ...')
                fo.write(os.path.join(a, l))
        fo.close()
    
    # Parsing the current JSON file.
    json_path = 'gkisplus.json'
    fi = open(json_path, 'r')
    j = json.load(fi)
    fi.close()
    
    # Incrementing the update count and updating the 'last update' item.
    # SOURCE: https://stackoverflow.com/a/27914405
    j['meta']['update-count'] += 1
    j['meta']['last-actor'] = 'GITHUB_ACTIONS'
    j['meta']['last-update'] = int( time.mktime(dt.now().timetuple()) )
    j['meta']['last-updated-item'] = 'carousel'
    
    # Resetting the JSON node.
    j['data']['carousel'] = {}
    # Enlisting the list of static directory node.
    print('Morphing the JSON data ...')
    for l in sorted( os.listdir('./carousel') ):
        # Creating a dict
        a = {}
        
        # Opening the make.json (mj) file.
        with open(f'carousel/{l}/make.json', 'r') as fi:
            mj = json.load(fi)
            
            # Appending important information from make.json
            a['banner'] = mj['banner']
            a['title'] = mj['title']
            a['type'] = mj['type']
            a['date-created'] = mj['date-created']
            
            # Case-specific, according to the carousel item's type.
            if a['type'] == 'article':
                a['article-url'] = mj['article-url']
            elif a['type'] == 'poster':
                a['poster-image'] = mj['poster-image']
                a['poster-caption'] = mj['poster-caption']
            elif a['type'] == 'yt':
                # First we obtain the YouTube video information/snippet using the API v3.
                b = get_yt_snippet( get_cleansed_video_id(mj['yt-link']) )
                
                # Then we copy the YT API v3 result into the JSON.
                for m in b.keys():
                    a[m] = b[m]
                
            fi.close()
        
        # Enlisting the node into the JSON file.
        print(f'Appending static node: {l}')
        j['data']['carousel'][l] = a
        
        # DEBUG:
        print(a)
    
    # Writing into the remote GitHub repo's file.
    # SOURCE: https://www.perplexity.ai/search/show-me-how-to-write-into-gith-YSsKLQ9wTGun0NGHscbNzw
    # SOURCE: https://stackoverflow.com/a/12309296
    print('Writing the JSON file ...')
    with open(json_path, 'w') as fo:
        json.dump(j, fo, ensure_ascii=False, indent=4)
        fo.close()
    
    # Logging out.
    print('-' * 25)
    print('Finished the automation!')
    print(f'Total script time: {dt.now() - t}')
    
if __name__ == "__main__":
    execute()

'''
SAMPLE JSON NODE:
"00_komisi_anak": {
    "banner": "",
    "title": "",
    "type": "",
    "date-created": "",
    "article-url": "",
    "poster-image": "",
    "poster-caption": "",
    "yt-title": "",
    "yt-date": "",
    "yt-desc": "",
    "yt-link": "",
    "yt-thumbnail": "",
    "yt-is_live": 0
}
'''
