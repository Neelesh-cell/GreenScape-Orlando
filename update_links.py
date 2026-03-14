import os

files = ['index.html', 'portfolio.html', 'contact.html', 'privacy.html']

for f in files:
    if not os.path.exists(f):
        continue
    with open(f, 'r', encoding='utf8') as file:
        content = file.read()
    
    # replace /v1/page.html -> /page.html
    # replace /v1/ -> /
    content = content.replace('href="/v1/', 'href="/')
    
    with open(f, 'w', encoding='utf8') as file:
        file.write(content)

print("Updated links")
