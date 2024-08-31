from datetime import datetime as dt
from lxml import etree
from lxml import html
import json
import requests as rq
import time

s = rq.Session()

def get_data():
    # Preamble logging.
    print('Beginning the automation script for updating data: SaRen Pagi')
    t = dt.now()
    
    # GKI Salatiga YouTube channel ID
    channelId = 'UC5cn_kPPnf-VUYFnB0N7MZg'
    
    # SOURCE: https://stackoverflow.com/a/55207539
    print(f'Getting the XML RSS feed: {channelId} ...')
    r = rq.get(f'https://www.youtube.com/feeds/videos.xml?channel_id={channelId}')
    c = html.fromstring(r.content)
    
    # The scraped YT video titles.
    s1 = [l.strip() for l in c.xpath('//entry/title/text()')]
    
    # The scraped YT video ID.
    s2 = [l.split(':')[2] for l in c.xpath('//entry/id/text()')]
    
    # The scraped YT upload date.
    s3 = [l.split('T')[0] for l in c.xpath('//entry/published/text()')]
    
    # The scraped YT video description.
    # SOURCE: https://stackoverflow.com/questions/5239685/xml-namespace-breaking-my-xpath
    s4 = [l.strip() for l in c.xpath('//entry//*[local-name()="media:description"]/text()')]
    
    # The scraped YT video URL.
    s5 = [l.strip() for l in c.xpath('//entry/link/@href')]
    
    # The scraped YT video thumbnail.
    s6 = [l.strip() for l in c.xpath('//entry//*[local-name()="media:thumbnail"]/@url')]
    
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
    j['meta']['last-updated-item'] = 'yt-video/saren'
    
    # Detecting which node is this playlist's
    node_title = 'Sapaan dan Renungan Pagi'
    k = j['data']['yt']['pinned'].copy()
    k.extend(j['data']['yt']['standard'])
    for a in k:
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
                if s1[i].lower().__contains__('saren pagi'):
                    print(f'Writing data no. {i}: {s1[i]}')
                    j['data']['yt'][parent_node][node_index]['content'].append({
                        'title': s1[i],
                        'date': s3[i],
                        'desc': s4[i],
                        'link': s5[i],
                        'thumbnail': s6[i],
                        'is_live': 0
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
