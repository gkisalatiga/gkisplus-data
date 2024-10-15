import json

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
    'verses_data': {
    }
}

with open('v2/modules/bible/engwebp_vpl.txt', 'r') as fi:
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
with open('v2/modules/bible/engwebp.json', 'w') as fo:
    fo.write(json.dumps(data, indent=4))
with open('v2/modules/bible/engwebp.min.json', 'w') as fo:
    fo.write(json.dumps(data, separators=(',', ':')))

print(len(data['verses_data']))
