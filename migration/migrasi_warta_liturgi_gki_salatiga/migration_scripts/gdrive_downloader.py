import pandas as pd
from urllib.request import urlretrieve

src='/ssynthesia/ghostcity/git-collab/gkisalatiga/gkisplus-data/migration/migrasi_warta_liturgi_gki_salatiga/url_liturgi.csv'
df = pd.read_csv(src)

download_directory='/ssynthesia/ghostcity/git-collab/gkisalatiga/gkisplus-data/migration/migrasi_warta_liturgi_gki_salatiga/downloaded_gdrive_pdf_liturgi/'

for i in range(len(df['url-page'])):
    if df['url-gdrive'][i] == 'special-case':
        pass
    else:
        print(df['title'][i], df['url-gdrive'][i])
        
        try:
            dl_id = df['url-gdrive'][i].split('file/d/')[1].split('/preview')[0]
            dl_link = f'http://drive.google.com/uc?id={dl_id}&export=download'
            urlretrieve(dl_link, download_directory + df['title'][i] + '.pdf')
            df['success'][i] = 'true'
        except:
            df['success'][i] = 'false'
            df.to_csv(src)
