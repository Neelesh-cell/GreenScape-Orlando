import os
from duckduckgo_search import DDGS
import requests

queries = {
    'images/landscaping/hero.jpg': 'luxury backyard professional landscaping patio green grass high resolution',
    'images/landscaping/lawn-care.jpg': 'perfectly manicured green residential lawn care yard',
    'images/landscaping/landscape-design.jpg': 'beautiful residential landscape design front yard garden beds',
    'images/landscaping/hardscaping.jpg': 'stone patio pavers backyard landscaping hardscape',
    'images/landscaping/irrigation.jpg': 'lawn sprinkler system watering green grass',
    'images/landscaping/tree-care.jpg': 'professional tree trimming landscaping yard work',
    'images/landscaping/landscaper.jpg': 'professional landscaping worker working in garden yard',
    'images/landscaping/portfolio-1.jpg': 'elegant walkway front yard landscaping',
    'images/landscaping/portfolio-2.jpg': 'modern outdoor living space patio backyard design',
    'images/landscaping/portfolio-3.jpg': 'stone paver walkway garden installation landscaping',
    'images/landscaping/portfolio-4.jpg': 'colorful floral garden bed landscape residential',
    'images/map.jpg': 'florida map stylized outline'
}

os.makedirs('images/landscaping', exist_ok=True)

for filename, query in queries.items():
    print(f"Searching for {filename}...")
    try:
        results = DDGS().images(query, max_results=5, size='Large')
        downloaded = False
        for res in results:
            url = res['image']
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(r.content)
                    print(f"Successfully downloaded {filename}")
                    downloaded = True
                    break
            except Exception as e:
                print(f"Failed to download {url}: {e}")
        if not downloaded:
            print(f"Could not download any image for {filename}")
    except Exception as e:
        print(f"Failed searching for {filename}: {e}")
