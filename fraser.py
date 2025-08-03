import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- Ayarlar ---
BASE_DOMAIN = 'https://fraser.stlouisfed.org'
BROWSE_URL  = BASE_DOMAIN + (
    '/title/federal-open-market-committee-meeting-minutes-transcripts-documents-677'
    '?browse=1930s'
)
# Eğer Drive’a kaydedeceksen üstteki DEST_DIR’ı kullan, 
# yoksa '/content/pdfs/1930s' de yazabilirsin:
DEST_DIR    = DEST_DIR  # daha önce tanımlı olmalı
DATES_FILE  = 'dates_1930s.txt'

threshold = datetime(1936, 3, 1)

# Çıktı klasörünü hazırla
os.makedirs(DEST_DIR, exist_ok=True)

# 1) Liste sayfasını çek
resp = requests.get(BROWSE_URL)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, 'html.parser')

# 2) Tarihleri parse et
dates = []
for a in soup.find_all('a'):
    t = a.get_text(strip=True)
    if t.startswith('Meeting,'):
        try:
            dt = datetime.strptime(t, 'Meeting, %B %d, %Y')
            dates.append(dt)
        except:
            continue

# 3) Tarihleri kaydet (opsiyonel)
with open(DATES_FILE, 'w') as f:
    for dt in dates:
        f.write(dt.strftime('%Y-%m-%d') + '\n')
print(f"{len(dates)} tarih bulundu, {DATES_FILE} dosyasına yazıldı.")

# 4) PDF’leri indir
for dt in dates:
    ymd = dt.strftime('%Y%m%d')
    if dt < threshold:
        name = f'rg82_fomcminutes_{ymd}.pdf'
    else:
        name = f'{ymd}Minutesv.pdf'
    url    = f"{BASE_DOMAIN}/files/docs/historical/FOMC/meetingdocuments/{name}"
    outpth = os.path.join(DEST_DIR, name)
    if os.path.exists(outpth):
        print("✔", name, "— zaten var")
        continue
    r = requests.get(url)
    if r.status_code == 200:
        with open(outpth, 'wb') as f:
            f.write(r.content)
        print("↓ İndirildi:", name)
    else:
        print("⨯ Bulunamadı:", name)

print("Tamamlandı. Dosyalar:", os.listdir(DEST_DIR)[:5], "…")
