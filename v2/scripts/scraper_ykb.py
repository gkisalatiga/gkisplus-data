from copy import deepcopy
from datetime import datetime as dt
from lxml import etree
from lxml import html
import json
import requests as rq
import time

s = rq.Session()

# Map of months used in the website's instance.
months_map = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12,
}

# Map of months in Indonesian
months_indonesian = [
    'Januari',
    'Februari',
    'Maret',
    'April',
    'Mei',
    'Juni',
    'Juli',
    'Agustus',
    'September',
    'Oktober',
    'November',
    'Desember',
]

# 2-digit zero-padding.
def zero_pad(l):
    if len(str(l)) == 0:
        return '00'
    elif len(str(l)) == 1:
        return f'0{l}'
    else:
        return l

def get_data():
    # Preamble logging.
    print('Beginning the automation script for updating data: Renungan YKB Wasiat')
    t = dt.now()
    
    ykb_links = [
        # 'https://www.ykb-wasiat.org/kiddy',
        #'https://www.ykb-wasiat.org/teens-for-christ',
        #'https://www.ykb-wasiat.org/youth-for-christ',
        'https://www.ykb-wasiat.org/wasiat',
        #'https://www.ykb-wasiat.org/jendela-hati'
    ]
    
    for a in ykb_links:
        r = s.get(a)
        c = html.fromstring(r.content)
        
        # The scraped devotional title
        s0 = [l.strip() for l in c.xpath('//div[@class="col-md-9 col-sm-9 col-xs-8 title-renungan"]/h4/text()')][0].title()
        
        # The scraped year
        s1 = [l.strip() for l in c.xpath('//table[@class="wp-calendar multiple-ajax-calendar-2"]/caption/text()')][0].split(' ')[1]
        
        # The scraped month
        s2 = [l.strip() for l in c.xpath('//div[@class="devotion-date-bulan"]/span/text()')][0]
        s2 = months_map[s2.lower()]
        s2 = zero_pad(s2)
        
        # The scraped day
        s3 = [l.strip() for l in c.xpath('//span[@class="devotion-date-tgl"]/text()')][0]
        s3 = zero_pad(s3)
        
        # The main HTML content
        s4 = c.xpath('//div[@class="renungan-padding content-devotion main-audio-xs"]')[0]
        
        # The scraped featured image.
        s5 = c.xpath('//div[@class="renungan-padding content-devotion main-audio-xs"]//figure//img/@src')
        
        # The scraped devotional scripture.
        s6 = c.xpath('//p[@class="has-text-align-center"]//strong/text()')[0]
        
        # Removing old (bloated!) image tag.
        if len(s5) > 0:
            s5 = s5[0]
            
            # Prepending with the cleansed image tag.
            new_img = html.Element('img', src=s5)
            
            xx = s4.getparent().xpath('.//figure')[0]
            yy = s4.getparent().xpath('.//figure')[0].xpath('.//figure')[0]
            zz = s4.getparent().xpath('.//figure')[0].xpath('.//figure')[0].xpath('.//img')[0]
            yy.remove(zz)
            xx.remove(yy)
            
            # Then place the new, cleansed image.
            xx.insert(0, new_img)
            
        else:
            s5 = ''
        
        # Wrap the scraped image around a container (and of course body tag!)
        tag_html = html.Element('html')
        tag_head = html.Element('head')
        tag_css = html.Element('style')
        tag_body = html.Element('body')
        tag_container = html.Element('div')
        
        tag_html.insert(0, tag_head)
        tag_html.insert(1, tag_body)
        tag_head.insert(0, tag_css)
        tag_body.insert(0, tag_container)
        
        tag_container.set('class', 'main-container')
        tag_container.insert(0, s4)
        
        # Append title
        tag_title = html.Element('h2')
        tag_title.text = s0
        tag_container.insert(0, tag_title)
        
        # Append date
        tag_date = html.Element('div')
        tag_date.set('class', 'date')
        tag_date.text = f'{str(int(s3))} {months_indonesian[int(s2) - 1]} {s1}'
        tag_container.insert(1, tag_date)
        
        with open('v2/static/stylesheet_ykb.css', 'r') as fi:
            tag_css.text = fi.read()
        
        # The export HTML content.
        c_export = deepcopy(tag_html)
        
        # Prettifying the export.
        c_export = html.tostring(c_export, method='html', encoding='utf-8').decode('utf-8')
        c_export = c_export.replace('<em> </em>', '').replace('<p> </p>', '')
        
        # Cleaning and prettifying
        while True:
            if c_export.__contains__('\n\n'):
                c_export = c_export.replace('\n\n', '')
            else:
                break
        
        # Whitespace cleaning.
        while True:
            if c_export.__contains__('  '):
                c_export = c_export.replace('  ', ' ')
            else:
                break
        
        # Tab stripping.
        while True:
            if c_export.__contains__('\t'):
                c_export = c_export.replace('\t', ' ')
            else:
                break
        
        c_export = c_export.strip()
        with open('a.html', 'w') as fo:
            fo.write(c_export)
        
        print(c_export)
        # print(s1, s2, s3, s4, s5)
    
    '''
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
    '''
    
    # ---------------------------------------------------------------------------------- #
    
    # Logging out.
    print('-' * 25)
    print('Finished the automation!')
    print(f'Total script time: {dt.now() - t}')
    
if __name__ == "__main__":
    get_data()
