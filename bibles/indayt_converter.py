import json
import xmltodict

# The aggregated data
data = {
    'meta': {
        'name': 'Alkitab Yang Terbuka',
        'abbr': 'AYT',
        'license': 'CC-BY-NC-SA-4.0',
        'license-url': 'https://spdx.org/licenses/CC-BY-NC-SA-4.0.html',
        'author': 'Yayasan Lembaga SABDA (YLSA)',
        'author-url': 'https://ylsa.org',
        'source': 'https://ebible.org/details.php?id=indayt',
        'description': 'AYT adalah keseluruhan sistem pembelajaran Alkitab (Bible Study Sistem) yang lengkap dan terintegrasi dengan Pustaka Terbuka serta Komunitas Terbuka dengan memanfaatkan perkembangan teknologi abad ke-21.',
    },
    'index': {},
    'verses': []
}

with open('bibles/indayt_usfx/BookNames.xml', 'r') as fi:
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

with open('bibles/indayt_vpl/indayt_vpl.txt', 'r') as fi:
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
with open('bibles/indayt.json', 'w') as fo:
    fo.write(json.dumps(data, indent=4))
with open('bibles/indayt.min.json', 'w') as fo:
    fo.write(json.dumps(data, separators=(',', ':')))
