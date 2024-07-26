from datetime import datetime as dt
from zipfile import ZipFile as zf
import json
import os
import time

def execute():
    # Preamble logging.
    print('Beginning the automation script for zipping the static data ...')
    t = dt.now()
    
    # Overwriting the zip archive file.
    # SOURCE: https://docs.python.org/3/library/zipfile.html
    print('Creating the ZIP archive and compressing ...')
    with zf('gkisplus-static.zip', mode='w', compression=8) as fo:
        
        # Recurse into the static folder.
        # SOURCE: https://docs.python.org/3/library/os.html
        '''
        Sample output of os.walk('static'):
        static ['00_profil_gereja', '10_pendeta', '20_majelis_jemaat', '30_badan_pelayanan', '40_pa_wilayah'] []
        static/00_profil_gereja [] ['gkisalatiga-2024.jpg', 'index.html', 'logo-gki-putih.png', 'styles.css']
        static/10_pendeta [] ['styles.css', 'img-sample.png', 'index.html', 'script.js']
        static/20_majelis_jemaat [] ['img-sample.png', 'index.html', 'script.js', 'styles.css']
        static/30_badan_pelayanan [] ['img-sample.png', 'index.html', 'script.js', 'styles.css']
        static/40_pa_wilayah [] ['img-sample.png', 'index.html', 'script.js', 'styles.css']
        '''
        for a, b, c in os.walk('static'):
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
    j['meta']['last-updated-item'] = 'static'
    
    # Resetting the JSON node.
    j['data']['static'] = {}
    # Enlisting the list of static directory node.
    print('Morphing the JSON data ...')
    for l in os.listdir('./static'):
        # Obtain this node's particular profile title.
        m = ''
        with open(f'./static/{l}/title.txt', 'r') as fi:
            for n in fi:
                m += n.strip()
            fi.close()
        
        # Enlisting the node into the JSON file.
        print(f'Appending static node: {l}')
        j['data']['static'][l] = m
    
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
