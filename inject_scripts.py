import os
from bs4 import BeautifulSoup

directory = '.'

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        head = soup.head
        body = soup.body
        
        # Check if AOS CSS is already added
        if not soup.find('link', href='https://unpkg.com/aos@2.3.1/dist/aos.css'):
            head.append(soup.new_tag('link', rel='stylesheet', href='https://unpkg.com/aos@2.3.1/dist/aos.css'))
        
        # Check if Swiper CSS is already added
        if not soup.find('link', href='https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css'):
            head.append(soup.new_tag('link', rel='stylesheet', href='https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css'))

        # Add global styles
        if not soup.find('style', id='custom-styles'):
            style_tag = soup.new_tag('style', id='custom-styles')
            style_tag.string = """
            body { overflow-x: hidden; }
            .mobile_nav_open { transform: translateX(0) !important; }
            .swiper { width: 100%; height: 100%; }
            .swiper-slide { background-position: center; background-size: cover; }
            """
            head.append(style_tag)
        
        # Add scripts to body
        if not soup.find('script', src='https://unpkg.com/aos@2.3.1/dist/aos.js'):
            body.append(soup.new_tag('script', src='https://unpkg.com/aos@2.3.1/dist/aos.js'))
        
        if not soup.find('script', src='https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js'):
            body.append(soup.new_tag('script', src='https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js'))
            
        if not soup.find('script', id='custom-scripts'):
            script_tag = soup.new_tag('script', id='custom-scripts')
            script_tag.string = """
            document.addEventListener('DOMContentLoaded', function() {
                // Initialize AOS
                AOS.init({
                    duration: 800,
                    easing: 'ease-in-out',
                    once: true,
                    mirror: false
                });
                
                // Initialize Swiper
                if (document.querySelector('.mySwiper') || document.querySelector('.home_banner')) {
                    new Swiper('.swiper', {
                        effect: 'fade',
                        fadeEffect: { crossFade: true },
                        autoplay: {
                            delay: 3500,
                            disableOnInteraction: false,
                        },
                        pagination: {
                            el: '.swiper-pagination',
                            clickable: true,
                        },
                        loop: true
                    });
                }
                
                // Mobile Menu Toggle
                const mobileMenuBtn = document.querySelector('.mobile_nav button');
                const mobileMenu = document.querySelector('.fixed.top-0.right-0.h-full.w-64');
                if (mobileMenuBtn && mobileMenu) {
                    mobileMenuBtn.addEventListener('click', () => {
                        mobileMenu.classList.toggle('translate-x-full');
                    });
                    
                    // Close menu when clicking outside
                    document.addEventListener('click', (e) => {
                        if (!mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                            mobileMenu.classList.add('translate-x-full');
                        }
                    });
                }
            });
            """
            body.append(script_tag)

        # Write the modified content back to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Added JS/CSS to {filename}")
