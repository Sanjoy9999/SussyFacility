import re
from bs4 import BeautifulSoup
import os

with open('note.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Split the content by the '=' separator
pages = re.split(r'={10,}\s*\n', content)

# Map section names to file names
page_mapping = {
    'Home': 'index.html',
    'service': 'services.html',
    'Recruitment': 'recruitment.html',
    'Training': 'training.html',
    'About': 'about.html',
    'Contact': 'contact.html'
}

for page in pages:
    page = page.strip()
    if not page:
        continue
    
    # The first line should be the page name
    lines = page.split('\n')
    page_name = lines[0].strip()
    
    if page_name in page_mapping:
        file_name = page_mapping[page_name]
        
        # The rest is the HTML
        html_content = '\n'.join(lines[1:]).strip()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove all darkreader styles
        for tag in soup.find_all(class_=re.compile("darkreader")):
            tag.decompose()
        
        # Remove data-darkreader-* attributes
        for tag in soup.find_all():
            attrs = list(tag.attrs.keys())
            for attr in attrs:
                if attr.startswith('data-darkreader-') or attr == 'data-darkreader-scheme' or attr == 'data-darkreader-mode':
                    del tag[attr]
        
        # Clean up html tag attributes specifically
        if soup.html:
            if 'data-darkreader-mode' in soup.html.attrs:
                del soup.html['data-darkreader-mode']
            if 'data-darkreader-scheme' in soup.html.attrs:
                del soup.html['data-darkreader-scheme']
            if 'data-darkreader-proxy-injected' in soup.html.attrs:
                del soup.html['data-darkreader-proxy-injected']
        
        # Add Tailwind CDN to head for quick styling
        head = soup.head
        if head:
            # We don't have the original CSS, so we inject tailwind CDN
            tailwind_script = soup.new_tag('script', src="https://cdn.tailwindcss.com")
            head.append(tailwind_script)
            
            # Remove the bundled scripts/css since they won't work locally without the assets
            for tag in head.find_all(['script', 'link']):
                if tag.get('src', '').startswith('/assets/') or tag.get('href', '').startswith('/assets/'):
                    tag.decompose()
        
        # Make all links point to .html files so it works locally without a complex server
        for tag in soup.find_all('a'):
            href = tag.get('href', '')
            if href == '/':
                tag['href'] = '/index.html'
            elif href.startswith('/') and not href.startswith('//') and not href.endswith('.html'):
                # if it's a simple route like /services, make it /services.html
                if len(href) > 1:
                    tag['href'] = href + '.html'
        
        with open(file_name, 'w', encoding='utf-8') as out_f:
            out_f.write(str(soup))
        print(f"Extracted {page_name} -> {file_name}")
