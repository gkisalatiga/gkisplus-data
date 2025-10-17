import json
import xmltodict

# The aggregated data
data = {
    'meta': {
        'name': 'Bible in Basic English',
        'abbr': 'BBE',
        'license': 'Public Domain',
        'license-url': 'https://www.bible-discovery.com/bible-license-bbe.php',
        'author': 'Samuel Henry Hooke, Cambridge Press',
        'author-url': 'https://ebible.org/find/show.php?id=engBBE',
        'source': 'https://ebible.org/find/show.php?id=engBBE',
        'description': 'The Bible In Basic English was printed in 1965 by Cambridge Press in England. Published without any copyright notice and distributed in America, this work fell immediately and irretrievably into the Public Domain in the United States according to the UCC convention of that time. A call to Cambridge prior to placing this work in etext resulted in an admission of this fact.',
    },
    'index': {},
    'verses': []
}

with open('bibles/engBBE_usfx/BookNames.xml', 'r') as fi:
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

with open('bibles/engBBE_vpl/engBBE_vpl.txt', 'r') as fi:
    for l in fi:
        # Get the infos.
        bok = l.split(maxsplit=2)[0]
        chp = l.split(maxsplit=2)[1].split(':')[0]
        vrs = l.split(maxsplit=2)[1].split(':')[1]
        txt = l.split(maxsplit=2)[2]
        
        # Initializing the dicts.
        data['verses'].append({
            'b': str(bok),
            'c': int(chp),
            'v': int(vrs),
            't': str(txt),
        })

# Write the aggregated data.
with open('bibles/engbbe.json', 'w') as fo:
    fo.write(json.dumps(data, indent=4))
with open('bibles/engbbe.min.json', 'w') as fo:
    fo.write(json.dumps(data, separators=(',', ':')))
