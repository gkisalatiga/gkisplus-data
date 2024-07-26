import json

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
    'verses_data': {
    }
}

with open('v2/modules/bible/engbbe_vpl.txt', 'r') as fi:
    for l in fi:
        # Get the verse ID.
        verse_id = f'{l.split()[0]} {l.split()[1]}'
        
        # Split verse ID into book name ID, chapter number, and verse number.
        id_b = verse_id.split()[0]
        id_c = verse_id.split()[1].split(':')[0]
        id_v = verse_id.split()[1].split(':')[1]
        
        # Get the verse content.
        verse_content = l.replace(verse_id, '', 1).strip()
        
        # Initializing the dicts.
        if type(data['verses_data']) is not dict:
            data['verses_data'] = {}
        if type(data['verses_data'].get(id_b, None)) is not dict:
            data['verses_data'][id_b] = {}
        if type(data['verses_data'][id_b].get(id_c, None)) is not dict:
            data['verses_data'][id_b][id_c] = {}
        
        # Forge the verse_id + verse_content data.
        data['verses_data'][id_b][id_c][id_v] = verse_content

# Write the aggregated data.
with open('v2/modules/bible/engbbe.json', 'w') as fo:
    fo.write(json.dumps(data, indent=4))
with open('v2/modules/bible/engbbe.min.json', 'w') as fo:
    fo.write(json.dumps(data, separators=(',', ':')))

print(len(data['verses_data']))
