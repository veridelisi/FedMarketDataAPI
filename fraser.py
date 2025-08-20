import os
import shutil
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- Settings ---
BASE_DOMAIN = 'https://fraser.stlouisfed.org'
BROWSE_URL  = BASE_DOMAIN + (
    '/title/federal-open-market-committee-meeting-minutes-transcripts-documents-677'
    '?browse=1930s'
)
DEST_DIR    = 'pdfs/1930s'
DATES_FILE  = 'dates_1930s.txt'

# Date threshold: March 1, 1936
threshold = datetime(1936, 3, 1)

# --- Helpers ---
def in_colab() -> bool:
    try:
        import google.colab  # type: ignore
        return True
    except Exception:
        return False

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

# More robust requests: session + header
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
})
TIMEOUT = 30

# --- 0) Prepare directory ---
ensure_dir(DEST_DIR)

# --- 1) Fetch and parse the page ---
resp = session.get(BROWSE_URL, timeout=TIMEOUT)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, 'html.parser')

# --- 2) Build datetimes from links like “Meeting, Month Day, Year” ---
dates = []
for a in soup.find_all('a'):
    text = a.get_text(strip=True)
    if text.startswith('Meeting,'):
        try:
            dt = datetime.strptime(text, 'Meeting, %B %d, %Y')
            dates.append(dt)
        except ValueError:
            # skip non-matching formats
            continue

# --- 3) Save dates as YYYY-MM-DD ---
with open(DATES_FILE, 'w', encoding='utf-8') as f:
    for dt in dates:
        f.write(dt.strftime('%Y-%m-%d') + '\n')
print(f"[✔] {len(dates)} meeting dates saved → {DATES_FILE}")

# --- 4) For each date, choose the correct filename and download ---
success, fail = 0, 0
for dt in dates:
    ymd = dt.strftime('%Y%m%d')

    # Before March 1, 1936: rg82_fomcminutes_YYYYMMDD.pdf
    # On/after March 1, 1936: YYYYMMDDMinutesv.pdf
    if dt < threshold:
        pdf_name = f'rg82_fomcminutes_{ymd}.pdf'
    else:
        pdf_name = f'{ymd}Minutesv.pdf'

    pdf_url = f"{BASE_DOMAIN}/files/docs/historical/FOMC/meetingdocuments/{pdf_name}"
    outpath = os.path.join(DEST_DIR, pdf_name)

    if os.path.exists(outpath):
        print(f"[●] Skipping (already exists): {pdf_name}")
        continue

    print(f"[↓] Downloading: {pdf_name}")
    r = session.get(pdf_url, timeout=TIMEOUT)
    if r.status_code == 200 and r.content.startswith(b'%PDF'):
        with open(outpath, 'wb') as f:
            f.write(r.content)
        success += 1
    else:
        print(f"  ⚠️  Error {r.status_code} while downloading: {pdf_url}")
        fail += 1

print(f"✅ Download finished. Success: {success}, Failed: {fail}")
print(f"📁 Folder: {os.path.abspath(DEST_DIR)}")

# --- 5) Create ZIP and optionally auto-download ---
zip_base = 'FOMC_1930s'
zip_path = shutil.make_archive(zip_base, 'zip', DEST_DIR)
print(f"🗜 ZIP ready: {zip_path}")

if in_colab():
    # Auto-download in Colab
    try:
        from google.colab import files
        files.download(zip_path)
        print("⬇️ Downloading ZIP (Colab).")
    except Exception as e:
        print(f"Colab auto-download error: {e}\nYou can download the ZIP manually from the left panel.")
else:
    print("You are running outside Colab. You can find the ZIP file at this path:")
    print(os.path.abspath(zip_path))
