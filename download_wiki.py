import requests
import os

queries = {
    'tree trimming arborist': 'tree-care.jpg',
    'landscaper working garden': 'landscaper.jpg',
    'florida map green outline graphic': 'map.jpg'  # might need generic if not found
}

def search_wikimedia(query, filename):
    print(f"Searching Wikimedia for {query}...")
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrlimit": 5,
        "iiprop": "url"
    }
    
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, params=params, headers=headers).json()
        pages = response.get('query', {}).get('pages', {})
        if pages:
            for page_id, page in pages.items():
                imageinfo = page.get('imageinfo', [{}])[0]
                image_url = imageinfo.get('url')
                if image_url:
                    r = requests.get(image_url, headers=headers)
                    if r.status_code == 200:
                        dest = os.path.join('images/landscaping', filename) if filename != 'map.jpg' else os.path.join('images', filename)
                        with open(dest, 'wb') as f:
                            f.write(r.content)
                        print(f"Downloaded {filename} from Wikimedia")
                        return True
        else:
            print(f"No results for {query} on Wikimedia.")
    except Exception as e:
        print(f"Error: {e}")
    return False

for query, filename in queries.items():
    success = search_wikimedia(query, filename)
    if not success:
        # fallback broader query
        search_wikimedia(query.split()[0], filename)
