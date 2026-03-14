import urllib.request
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
    req = urllib.request.Request(
        f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # find all src="//v.gif..." or image links
        # duckduckgo html image results are linked via <img class="result__icon__img" src="//..." />
        matches = re.findall(r'<img[^>]+src="([^">]+)"', html)
        downloaded = False
        for src in matches:
            if src.startswith('//'):
                src = 'https:' + src
            if src.startswith('http'):
                try:
                    r_img = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
                    img_data = urllib.request.urlopen(r_img, timeout=5).read()
                    with open(filename, 'wb') as f:
                        f.write(img_data)
                    print(f"Successfully scraped {filename}")
                    downloaded = True
                    break
                except Exception as e:
                    pass
        if not downloaded:
            print(f"No image found for {filename}")
    except Exception as e:
        print(f"Error for {filename}: {e}")
