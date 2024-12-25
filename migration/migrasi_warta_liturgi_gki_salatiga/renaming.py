src = '/ssynthesia/ghostcity/git-collab/gkisalatiga/gkisplus-data/migration/migrasi_warta_liturgi_gki_salatiga/renaming_warta.csv'

month_map = {
    'januari': '01',
    'februari': '02',
    'maret': '03',
    'april': '04',
    'mei': '05',
    'juni': '06',
    'juli': '07',
    'agustus': '08',
    'september': '09',
    'oktober': '10',
    'november': '11',
    'desember': '12',
}

def zero_pad_two(i: int):
    if i < 10:
        return '0' + str(i)
    else:
        return str(i)

with open(src, 'r') as fi:
    for l in fi:
        try:
            s = l.split(',')[0].replace('Warta Jemaat', '').strip().split(' ')
            # s = l.split(',')[0].split(' ')[4:]
            #print(s.split(' '))
            s0 = s[0]
            s1 = s[1]
            s2 = s[2]
            #print(f'{s2}-{s1}-{s0}')
            s_mon = month_map[str(s1.lower())]
            #print(s_mon)
            #print(month_map[str(s1.lower())])
            print(f'{s2}-{s_mon}-{zero_pad_two(int(s0))}')
        except:
            print('>')
            continue
