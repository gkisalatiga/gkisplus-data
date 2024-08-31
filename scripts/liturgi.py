from datetime import datetime as dt
from lxml import html
import json
import requests as rq
import time

s = rq.Session()

def get_data():
    # Preamble logging.
    print('Beginning the automation script for updating data: Tata Ibadah')
    t = dt.now()
    
    scrape_url = 'https://gkisalatiga.org/category/tata-ibadah'
    print(f'Getting the URL: {scrape_url} ...')
    r = s.get(scrape_url)
    c = html.fromstring(r.content)
    
    base_xpath = '//header[@class="entry-header"]'
    
    # The scraped post page links.
    s1 = c.xpath(base_xpath + '/h1[@class="entry-title"]/a/@href')
    
    # The scraped church news title.
    s2 = c.xpath(base_xpath + '/h1[@class="entry-title"]/a/text()')
    
    # The scraped post upload date.
    s3 = c.xpath(base_xpath + '/div[@class="entry-meta"]/span[@class="posted-on"]//time[@class="entry-date published"]/@datetime')
    
    print('Now retrieving the Google Drive links ...')
    # The scraped church news Google Drive links.
    s4 = []
    for l in s1:
        print(f'Iterating: {l}')
        r = s.get(l)
        c = html.fromstring(r.content)
        u = c.xpath('//div[@id="primary"]//iframe[@allow="autoplay"]/@src')[0]
        print(f'--- Retrieved the URL: {u}')
        s4.append(u)
    
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
    j['meta']['last-updated-item'] = 'pdf/liturgi'
    
    # Resetting the JSON node.
    j['data']['pdf']['liturgi'] = []
    # Assumes identical s1, s2 and s3 list size.
    # Writes the scraped data into the JSON file.
    print('Morphing the JSON data ...')
    for i in range(len(s1)):
        print(f'Writing data no. {i}: {s2[i]}')
        j['data']['pdf']['liturgi'].append({
            'title': s2[i],
            'date': s3[i].split('T')[0].strip(),
            'link': s4[i],
            'post-page': s1[i],
            # We leave the thumbnail item blank for now, since it is not used in the app.
            'thumbnail': ''
        })
    
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
