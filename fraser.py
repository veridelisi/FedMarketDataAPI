import os
import shutil
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- Ayarlar ---
BASE_DOMAIN = 'https://fraser.stlouisfed.org'
BROWSE_URL  = BASE_DOMAIN + (
    '/title/federal-open-market-committee-meeting-minutes-transcripts-documents-677'
    '?browse=1930s'
)
DEST_DIR    = 'pdfs/1930s'
DATES_FILE  = 'dates_1930s.txt'

# Tarih eşiği: 1 Mart 1936
threshold = datetime(1936, 3, 1)

# --- Yardımcılar ---
def in_colab() -> bool:
    try:
        import google.colab  # type: ignore
        return True
    except Exception:
        return False

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

# Daha sağlam istekler için session + header
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
})
TIMEOUT = 30

# --- 0) Klasörü hazırla ---
ensure_dir(DEST_DIR)

# --- 1) Sayfayı indir ve parse et ---
resp = session.get(BROWSE_URL, timeout=TIMEOUT)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, 'html.parser')

# --- 2) “Meeting, Month Day, Year” linklerinden datetime’lar oluştur ---
dates = []
for a in soup.find_all('a'):
    text = a.get_text(strip=True)
    if text.startswith('Meeting,'):
        try:
            dt = datetime.strptime(text, 'Meeting, %B %d, %Y')
            dates.append(dt)
        except ValueError:
            # format tutmayanları atla
            continue

# --- 3) Tarihleri YYYY-MM-DD olarak kaydet ---
with open(DATES_FILE, 'w', encoding='utf-8') as f:
    for dt in dates:
        f.write(dt.strftime('%Y-%m-%d') + '\n')
print(f"[✔] {len(dates)} toplantı tarihi kaydedildi → {DATES_FILE}")

# --- 4) Her tarih için doğru dosya adını seçip indir ---
success, fail = 0, 0
for dt in dates:
    ymd = dt.strftime('%Y%m%d')

    # 1 Mart 1936 öncesi: rg82_fomcminutes_YYYYMMDD.pdf
    # 1 Mart 1936 ve sonrası: YYYYMMDDMinutesv.pdf
    if dt < threshold:
        pdf_name = f'rg82_fomcminutes_{ymd}.pdf'
    else:
        pdf_name = f'{ymd}Minutesv.pdf'

    pdf_url = f"{BASE_DOMAIN}/files/docs/historical/FOMC/meetingdocuments/{pdf_name}"
    outpath = os.path.join(DEST_DIR, pdf_name)

    if os.path.exists(outpath):
        print(f"[●] Atlanıyor (zaten var): {pdf_name}")
        continue

    print(f"[↓] İndiriliyor: {pdf_name}")
    r = session.get(pdf_url, timeout=TIMEOUT)
    if r.status_code == 200 and r.content.startswith(b'%PDF'):
        with open(outpath, 'wb') as f:
            f.write(r.content)
        success += 1
    else:
        print(f"  ⚠️  Hata {r.status_code} indirirken: {pdf_url}")
        fail += 1

print(f"✅ İndirme tamamlandı. Başarılı: {success}, Başarısız: {fail}")
print(f"📁 Klasör: {os.path.abspath(DEST_DIR)}")

# --- 5) ZIP oluştur ve gerekirse otomatik indir ---
zip_base = 'FOMC_1930s'
zip_path = shutil.make_archive(zip_base, 'zip', DEST_DIR)
print(f"🗜 ZIP hazır: {zip_path}")

if in_colab():
    # Colab'da otomatik indir
    try:
        from google.colab import files
        files.download(zip_path)
        print("⬇️ ZIP indiriliyor (Colab).")
    except Exception as e:
        print(f"Colab otomatik indirme hatası: {e}\nZIP dosyasını sol panelden manuel indirebilirsiniz.")
else:
    print("Colab dışında çalışıyorsunuz. ZIP dosyasını bu yoldan bulabilirsiniz:")
    print(os.path.abspath(zip_path))
