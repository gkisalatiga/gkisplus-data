import json
import requests as rq
import sys


prefix_local = 'v2/data/'
prefix_remote = 'https://raw.githubusercontent.com/gkisalatiga/gkisplus-data-json/main/v2/data/'
sources = [
    'feeds.json',
    'feeds.min.json',
    'gkisplus-gallery.json',
    'gkisplus-gallery.min.json',
    'gkisplus-main.json',
    'gkisplus-main.min.json',
    'gkisplus-modules.json',
    'gkisplus-modules.min.json',
    'gkisplus-static.json',
    'gkisplus-static.min.json',
]

exit_code_zero = False
for l in sources:
    # Remote change.
    r = rq.get(prefix_remote + l)
    c = r.content.decode()
    j = json.loads(c)
    
    # Local file.
    with open(prefix_local + l, 'r') as fi:
        j_loc = json.load(fi)
    
    # Applying change/difference.
    print(f'Mirroring {l}: {j_loc != j}')
    if j_loc != j:
        exit_code_zero = True
        with open(prefix_local + l, 'w') as fo:
            if l.__contains__('.min.json'):
                json.dump(j, fo, separators=(',', ':'))
            else:
                json.dump(j, fo, indent=4)
    
print(f'Exit with code zero: {exit_code_zero}')
sys.exit(0 if exit_code_zero else 234)
