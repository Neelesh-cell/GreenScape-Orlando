import os
import time
from duckduckgo_search import DDGS
import requests

missing_queries = {
    'images/landscaping/tree-care.jpg': 'tree pruning arborist worker',
    'images/landscaping/landscaper.jpg': 'landscaper planting flowers garden',
    'images/map.jpg': 'florida state map outline graphic'
}

for filename, query in missing_queries.items():
    if os.path.exists(filename):
        continue
    print(f"Searching for {filename}...")
    try:
        results = DDGS().images(query, max_results=5)
        downloaded = False
        for res in results:
            url = res['image']
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                r = requests.get(url, headers=headers, timeout=5)
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
    time.sleep(5)
