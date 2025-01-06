import json
import os

base = 'profiles'
base_out = 'profiles/json-sanitized'

for l in os.listdir(base):
    if l.endswith('.html'):
        print('Sanitizing:', l)
        
        with open(base + os.sep + l, 'r') as fi:
            m = fi.read()
            j = json.dumps(m)
            
            with open(base_out + os.sep + l.replace('.html', '.json'), 'w') as fo:
                fo.write(j)
