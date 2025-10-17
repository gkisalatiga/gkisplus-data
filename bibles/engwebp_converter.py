import json
import xmltodict

# The aggregated data
data = {
    'meta': {
        'name': 'World English Bible',
        'abbr': 'WEB',
        'license': 'Public Domain',
        'license-url': 'https://worldenglish.bible',
        'author': 'Michael Paul Johnson',
        'author-url': 'https://mljohnson.org',
        'source': 'https://ebible.org/find/show.php?id=engwebp',
        'description': 'The World English Bible is a Public Domain translation of the Holy Bible into modern English.',
    },
    'index': {},
    'verses': []
}

with open('bibles/engwebp_usfx/BookNames.xml', 'r') as fi:
    raw = fi.readlines()[0]
    xml = xmltodict.parse(raw)
    for l in xml['BookNames']['book']:
        data['index'][l['@code']] = {
            'code': l['@code'],
            'abbr': l['@abbr'],
            'short': l['@short'],
            'long': l['@long'],
            'alt': l['@alt'],
        }

with open('bibles/engwebp_vpl/engwebp_vpl.txt', 'r') as fi:
    for l in fi:
        # Get the infos.
        bok = l.split(maxsplit=2)[0]
        chp = l.split(maxsplit=2)[1].split(':')[0]
        vrs = l.split(maxsplit=2)[1].split(':')[1]
        
        if len(l.split(maxsplit=2)) == 2:
            txt = '[[EMPTY]]'
        else:
            txt = l.split(maxsplit=2)[2]
        
        # Initializing the dicts.
        data['verses'].append({
            'b': str(bok),
            'c': int(chp),
            'v': int(vrs),
            't': str(txt),
        })

# Write the aggregated data.
with open('bibles/engwebp.json', 'w') as fo:
    fo.write(json.dumps(data, indent=4))
with open('bibles/engwebp.min.json', 'w') as fo:
    fo.write(json.dumps(data, separators=(',', ':')))
