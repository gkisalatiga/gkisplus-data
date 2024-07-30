from datetime import datetime as dt
import json
import os
import tarfile as tf
import time

def execute():
    # Preamble logging.
    print('Beginning the automation script for zipping the static data ...')
    t = dt.now()
    
    # Overwriting the tar archive file.
    # SOURCE: https://docs.python.org/3/library/tarfile.html
    print('Creating the TAR-GZIP archive and compressing ...')
    with tf.open('static.tar.gz', mode='w:gz', compresslevel=9) as fo:
        fo.add('static', recursive=True)
        fo.close()
    
    # Parsing the current JSON file.
    json_path = 'gkisplus.json'
    fi = open(json_path, 'r')
    j = json.load(fi)
    fi.close()
    
    # Incrementing the update count and updating the 'last update' item.
    # SOURCE: https://stackoverflow.com/a/27914405
    j['meta']['update-count'] += 1
    j['meta']['last-update'] = int( time.mktime(dt.now().timetuple()) )
    j['meta']['last-updated-item'] = 'static'
    
    # Resetting the JSON node.
    j['data']['static'] = []
    # Enlisting the list of static directory node.
    print('Morphing the JSON data ...')
    for l in os.listdir('./static'):
        print(f'Appending static node: {l}')
        j['data']['static'].append(l)
    
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
