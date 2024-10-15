import json

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
    'verses_data': {
    }
}

with open('v2/modules/bible/indayt_vpl.txt', 'r') as fi:
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
with open('v2/modules/bible/indayt.json', 'w') as fo:
    fo.write(json.dumps(data, indent=4))
with open('v2/modules/bible/indayt.min.json', 'w') as fo:
    fo.write(json.dumps(data, separators=(',', ':')))

print(len(data['verses_data']))
