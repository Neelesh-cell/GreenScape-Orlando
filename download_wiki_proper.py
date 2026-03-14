import requests
import os

queries = {
    'Tree pruning': 'tree-care.jpg',
    'Landscaper': 'landscaper.jpg',
    'Florida map': 'map.jpg'
}

def download_wiki(query, filename):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "gsrlimit": 10,
        "prop": "imageinfo",
        "iiprop": "url|size"
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, params=params, headers=headers).json()
    pages = r.get('query', {}).get('pages', {})
    for pid, page in pages.items():
        if 'imageinfo' in page:
            for info in page['imageinfo']:
                if info['url'].lower().endswith(('.jpg', '.jpeg', '.png')) and info['size'] > 50000:
                    img_url = info['url']
                    print(f"Downloading {img_url} for {filename}")
                    img_data = requests.get(img_url, headers=headers).content
                    dest = os.path.join('images/landscaping', filename) if filename != 'map.jpg' else os.path.join('images', filename)
                    with open(dest, 'wb') as f:
                        f.write(img_data)
                    return True
    return False

for query, filename in queries.items():
    success = download_wiki(query, filename)
    if not success:
        # try broader
        download_wiki(query.split()[0], filename)
