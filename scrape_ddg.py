import requests
from bs4 import BeautifulSoup
import re
import os

queries = {
    'images/landscaping/tree-care.jpg': 'tree pruning worker arborist landscaping',
    'images/landscaping/landscaper.jpg': 'landscaper planting flowers worker',
    'images/map.jpg': 'florida outline map graphic green'
}

for filename, query in queries.items():
    if os.path.exists(filename):
        continue
    print(f"Scraping HTML for {filename}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # DuckDuckGo HTML puts images in <img class="zcm__images"...> or inside links
        # Actually in HTML version, images are in <a> tags or <img> tags
        img_tags = soup.find_all('img')
        downloaded = False
        for img in img_tags:
            src = img.get('src')
            if src and src.startswith('//'):
                src = 'https:' + src
                # It's usually a thumbnail, but it's better than nothing and avoids 404
                img_r = requests.get(src, headers=headers)
                if img_r.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(img_r.content)
                    print(f"Successfully scraped {filename}")
                    downloaded = True
                    break
        if not downloaded:
            print(f"No image found for {filename}")
    except Exception as e:
        print(f"Error for {filename}: {e}")
