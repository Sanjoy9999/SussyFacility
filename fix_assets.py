import os

directory = '.'
base_url = 'https://lightgoldenrodyellow-skunk-171263.hostingersite.com'

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace local asset paths with absolute URLs
        content = content.replace('src="/assets/', f'src="{base_url}/assets/')
        content = content.replace('href="/assets/', f'href="{base_url}/assets/')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated paths in {filename}")
