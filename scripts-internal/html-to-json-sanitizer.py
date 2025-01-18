import json
import os
import re

base = 'profiles'
base_out = 'profiles/json-sanitized'

for l in os.listdir(base):
    if l.endswith('.html'):
        print('Sanitizing:', l)
        
        with open(base + os.sep + l, 'r') as fi:
            m = fi.read()
            
            # Remove comments.
            # SOURCE: https://stackoverflow.com/a/28208465
            m = re.sub('(<!--.*?-->)', '', m, flags=re.DOTALL)
            m = re.sub('(/\\*.*?\\*/)', '', m, flags=re.DOTALL)
            
            # Remove new line characters.
            m = m.replace('\n', '')
            
            # Remove double spaces.
            while True:
                if m.__contains__('  '):
                    m = m.replace('  ', ' ')
                else:
                    break
            
            j = json.dumps(m)
            
            with open(base_out + os.sep + l.replace('.html', '.json'), 'w') as fo:
                fo.write(j)
