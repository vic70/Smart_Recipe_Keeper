import re
from typing import Dict, Any
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from . import BaseExtractor, ContentType, ExtractorFactory


class WebsiteExtractor(BaseExtractor):
    """Extractor for general website URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    async def extract(self, url: str) -> Dict[str, Any]:
        """Extract content from a website URL"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract basic metadata
            title = self._extract_title(soup)
            description = self._extract_description(soup)
            images = self._extract_images(soup, url)
            
            # Extract recipe-specific data if available (schema.org)
            recipe_data = self._extract_recipe_schema(soup)
            
            # Extract raw text content for Gemini processing
            text_content = self._extract_text_content(soup)
            
            return {
                "url": url,
                "title": title,
                "description": description,
                "images": images,
                "recipe_data": recipe_data,
                "raw_content": text_content,
                "content_type": self.content_type.value
            }
        except Exception as e:
            raise Exception(f"Failed to extract content from {url}: {str(e)}")
    
    def can_handle(self, url: str) -> bool:
        """Check if this is a valid website URL"""
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except:
            return False
    
    @property
    def content_type(self) -> ContentType:
        return ContentType.WEBSITE
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        # Try og:title
        og_title = soup.find('meta', property='og:title')
        if og_title:
            return og_title.get('content', '')
        
        # Try h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        return ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract page description"""
        # Try meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '')
        
        # Try og:description
        og_desc = soup.find('meta', property='og:description')
        if og_desc:
            return og_desc.get('content', '')
        
        return ""
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        """Extract images from the page"""
        images = []
        
        # Try og:image first
        og_image = soup.find('meta', property='og:image')
        if og_image:
            images.append(og_image.get('content', ''))
        
        # Get other images
        img_tags = soup.find_all('img', src=True)[:5]  # Limit to 5 images
        for img in img_tags:
            src = img['src']
            if src.startswith('http'):
                images.append(src)
            elif src.startswith('/'):
                images.append(f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}{src}")
        
        return list(set(images))  # Remove duplicates
    
    def _extract_recipe_schema(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract recipe data from schema.org markup"""
        scripts = soup.find_all('script', type='application/ld+json')
        
        for script in scripts:
            try:
                import json
                data = json.loads(script.string)
                
                # Check if it's a recipe schema
                if isinstance(data, dict) and data.get('@type') == 'Recipe':
                    return data
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get('@type') == 'Recipe':
                            return item
            except:
                continue
        
        return {}
    
    def _extract_text_content(self, soup: BeautifulSoup) -> str:
        """Extract readable text content from the page"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading/trailing space
        lines = (line.strip() for line in text.splitlines())
        
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limit text length for API calls
        return text[:10000]


# Register the extractor
ExtractorFactory.register(WebsiteExtractor())