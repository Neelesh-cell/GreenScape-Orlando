from bing_image_downloader import downloader
import os
import shutil

queries = {
    'professional tree trimming arborist': 'tree-care.jpg',
    'landscaper working garden planting': 'landscaper.jpg',
    'state of florida map green graphic': 'map.jpg'
}

for query, filename in queries.items():
    print(f"Downloading {filename} for query '{query}'")
    try:
        downloader.download(query, limit=1, output_dir='bing_images', adult_filter_off=False, force_replace=True, timeout=10)
        
        # move file
        downloaded_dir = os.path.join('bing_images', query)
        if os.path.exists(downloaded_dir):
            files = os.listdir(downloaded_dir)
            if files:
                src = os.path.join(downloaded_dir, files[0])
                dest = os.path.join('images/landscaping', filename) if filename != 'map.jpg' else os.path.join('images', filename)
                shutil.copy(src, dest)
                print(f"Copied {filename}")
    except Exception as e:
        print(f"Failed {filename}: {e}")
