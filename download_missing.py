import os
import time
from duckduckgo_search import DDGS
import requests

missing_queries = {
    'images/landscaping/landscape-design.jpg': 'beautiful residential landscape design front yard garden beds',
    'images/landscaping/tree-care.jpg': 'professional tree trimming landscaping yard work',
    'images/landscaping/landscaper.jpg': 'professional landscaping worker working in garden yard',
    'images/landscaping/portfolio-4.jpg': 'colorful floral garden bed landscape residential',
    'images/map.jpg': 'florida map stylized outline green'
}

for filename, query in missing_queries.items():
    if os.path.exists(filename):
        continue
    print(f"Searching for {filename}...")
    try:
        results = DDGS().images(query, max_results=3)
        downloaded = False
        for res in results:
            url = res['image']
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(r.content)
                    print(f"Successfully downloaded {filename}")
                    downloaded = True
                    break
            except Exception as e:
                pass
        if not downloaded:
            print(f"Could not download {filename}")
    except Exception as e:
        print(f"Failed {filename}: {e}")
    time.sleep(3)
