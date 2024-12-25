import os

#src = '/ssynthesia/ghostcity/git-collab/gkisalatiga/gkisplus-data/migration/migrasi_warta_liturgi_gki_salatiga/renaming_warta.csv'
src = '/ssynthesia/ghostcity/git-collab/gkisalatiga/gkisplus-data/migration/migrasi_warta_liturgi_gki_salatiga/renaming_liturgi.csv'

#base = '/ssynthesia/ghostcity/git-collab/gkisalatiga/gkisplus-data/migration/migrasi_warta_liturgi_gki_salatiga/downloaded_gdrive_pdf_warta_jemaat/'
base = '/ssynthesia/ghostcity/git-collab/gkisalatiga/gkisplus-data/migration/migrasi_warta_liturgi_gki_salatiga/downloaded_gdrive_pdf_liturgi/'

with open(src, 'r') as fi:
    for l in fi:
        s = l.split(',')[0] + '.pdf'
        print(os.path.exists(base + s), s)