from datetime import datetime as dt
from lxml import etree
from lxml import html
import json
import os
import requests as rq
import time

s = rq.Session()

# The YouTube v3 API key.
print('Retrieving the API KEY secrets ...')
api_key = os.environ['YT_API_KEY']

def get_data():
    # Preamble logging.
    print('Beginning the automation script for updating data: Kebaktian Umum')
    t = dt.now()
    
    # GKI Salatiga channel's "Kebaktian Umum" playlist ID
    playlistId = 'PLtAv1OZRTdvI1P3YIJ4_qOqapZjV1PtnI'
    
    # Preparing the request queries.
    part = 'snippet'
    maxResults = 20
    
    # The Google API v3 bridge.
    bridge = 'https://www.googleapis.com/youtube/v3/playlistItems'
    
    # SOURCE: https://stackoverflow.com/a/55207539
    print(f'Getting the video data for playlist: {playlistId} ...')
    r = rq.get(bridge + f'?key={api_key}&part={part}&playlistId={playlistId}&maxResults={maxResults}')
    
    # The scraped YT video titles.
    s1 = []
    
    # The scraped YT video ID.
    s2 = []
    
    # The scraped YT upload date.
    s3 = []
    
    # The scraped YT video description.
    s4 = []
    
    # The scraped YT video URL.
    s5 = []
    
    # The scraped YT video thumbnail.
    s6 = []
    
    # Parsing the response JSON string.
    i = 0
    for a in r.json()['items']:
        videoId = a['snippet']['resourceId']['videoId']
        print(f'--- Iteration {i}; obtaining metadata for video ID: {videoId}')
        
        if a['snippet']['thumbnails'] == {}:
            print('..... Cannot retrieve video thumbnail because the video is private. Skipping ...')
            i += 1
            continue
        
        s1.append(a['snippet']['title'])
        s2.append(videoId)
        s3.append(a['snippet']['publishedAt'].split('T')[0])
        s4.append(a['snippet']['description'].strip())
        s5.append(f'https://www.youtube.com/watch?v={videoId}')
        s6.append(a['snippet']['thumbnails']['high']['url'])
        
        i += 1
    
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
    j['meta']['last-updated-item'] = 'yt-video/umum'
    
    # Detecting which node is this playlist's
    node_title = 'Kebaktian Umum'
    k = j['data']['yt']['pinned'].copy()
    k.extend(j['data']['yt']['standard'])
    for a in k:
        print(json.dumps(k[0], indent=2))
        if not a['title'] == node_title:
            continue
        else:
            # Detecting which parent node this playlist node belongs to.
            for x in ['pinned', 'standard']:
                if j['data']['yt'][x].__contains__(a):
                    parent_node = x
                    node_index = j['data']['yt'][x].index(a)
            
            # Resetting the JSON node.
            j['data']['yt'][parent_node][node_index]['content'] = []
            # Assumes identical s1, s2 and s3 list size.
            # Writes the scraped data into the JSON file.
            print('Morphing the JSON data ...')
            for i in range(len(s1)):
                print(f'Writing data no. {i}: {s1[i]}')
                j['data']['yt'][parent_node][node_index]['content'].append({
                    'title': s1[i],
                    'date': s3[i],
                    'desc': s4[i],
                    'link': s5[i],
                    'thumbnail': s6[i],
                    'is_live': 1
                })
            
            break
    
    # Writing into the remote GitHub repo's file.
    # SOURCE: https://www.perplexity.ai/search/show-me-how-to-write-into-gith-YSsKLQ9wTGun0NGHscbNzw
    # SOURCE: https://stackoverflow.com/a/12309296
    print('Writing the JSON file ...')
    with open(json_path, 'w') as fo:
        json.dump(j, fo, ensure_ascii=False, indent=4)
        fo.close()
    
    # ------------------------------- UPDATING THE FEEDS ------------------------------- #
    
    # Parsing the current JSON file.
    json_path = 'feeds.json'
    fi = open(json_path, 'r')
    j = json.load(fi)
    fi.close()
    
    # Incrementing the update count and updating the 'last update' item.
    j['feeds']['last-maindata-update'] = int( time.mktime(dt.now().timetuple()) )
    
    # Writing into the remote GitHub repo's file.
    print('Writing the JSON file ...')
    with open(json_path, 'w') as fo:
        json.dump(j, fo, ensure_ascii=False, indent=4)
        fo.close()
    
    # ---------------------------------------------------------------------------------- #
    
    # Logging out.
    print('-' * 25)
    print('Finished the automation!')
    print(f'Total script time: {dt.now() - t}')
    
if __name__ == "__main__":
    # Added fail-safe for internet lost.
    max_tries = 50
    wait_timeout = 2
    for i in range(max_tries):
        try:
            get_data()
            break
        except:
            time.sleep(wait_timeout)
            continue
