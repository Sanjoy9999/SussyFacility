import os
from bs4 import BeautifulSoup

directory = '.'

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Update custom styles
        style_tag = soup.find('style', id='custom-styles')
        if style_tag:
            new_css = """
            body { overflow-x: hidden; }
            .mobile_nav_open { transform: translateX(0) !important; }
            .swiper { width: 100%; height: 100%; }
            .swiper-slide { background-position: center; background-size: cover; }
            
            /* Header Fixes - Accurate Height & Alignment */
            header {
                background-color: transparent !important;
                height: 92px !important;
                transition: all 0.3s ease;
                z-index: 50;
            }
            
            .header_container {
                position: relative;
                z-index: 1;
                height: 60px !important; /* Total header 92px minus 32px of parent padding (py-4) */
                max-width: 1108px !important;
                margin: 0 auto !important;
                display: flex !important;
                align-items: center !important;
            }
            
            @media (min-width: 768px) {
                .header_container::after {
                    content: "";
                    position: absolute;
                    top: -16px; /* Overlap the py-4 padding */
                    bottom: -16px;
                    left: 20%; 
                    width: 150vw; 
                    background: linear-gradient(270deg, #a80000 0%, #1a1a1a 100%);
                    clip-path: polygon(10% 0, 100% 0, 100% 100%, 0 100%);
                    z-index: -1;
                }
                .mobile_nav {
                    display: none !important;
                }
            }
            
            @media (max-width: 767px) {
                header {
                    background-color: #1a1a1a !important;
                }
            }
            
            .logobox, .desktop_nav, .desktop_quote_btn {
                position: relative;
                z-index: 10;
            }
            .logobox {
                background-color: transparent;
                display: flex;
                align-items: center;
                height: 100%;
            }
            
            /* Quote Button Styling */
            .quote_btn {
                background-color: #000 !important;
                border: 1px solid #fff !important;
                color: #fff !important;
                padding: 10px 24px !important;
                height: 47px;
                display: flex;
                align-items: center;
                gap: 8px;
                font-weight: 600;
                border-radius: 5px;
                transition: all 0.3s ease;
            }
            .quote_btn:hover {
                background-color: #a80000 !important;
                border-color: #a80000 !important;
            }
            
            /* Navigation Typography & Hover */
            .desktop_nav a {
                font-family: 'Montserrat', sans-serif;
                font-size: 14px;
                font-weight: 600;
                position: relative;
                color: white !important;
            }
            .desktop_nav a.active::after, .desktop_nav a:hover::after {
                content: "";
                position: absolute;
                bottom: -5px;
                left: 0;
                width: 100%;
                height: 2px;
                background: white;
            }
            
            /* Scroll Sticky Header */
            .header-scrolled {
                position: fixed !important;
                top: 0;
                left: 0;
                width: 100%;
                height: 92px !important;
                z-index: 50;
                background-color: white !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                animation: slideDown 0.3s ease-in-out forwards;
            }
            @keyframes slideDown {
                from { transform: translateY(-100%); }
                to { transform: translateY(0); }
            }
            """
            style_tag.string = new_css
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Fixed sticky height in {filename}")
