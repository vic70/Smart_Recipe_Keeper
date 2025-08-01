from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum


class ContentType(Enum):
    WEBSITE = "website"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    MANUAL = "manual"


class BaseExtractor(ABC):
    """Base class for all content extractors"""
    
    @abstractmethod
    async def extract(self, url: str) -> Dict[str, Any]:
        """Extract content from the given URL"""
        pass
    
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Check if this extractor can handle the given URL"""
        pass
    
    @property
    @abstractmethod
    def content_type(self) -> ContentType:
        """Return the type of content this extractor handles"""
        pass


class ExtractorFactory:
    """Factory class to get the appropriate extractor for a URL"""
    
    _extractors: list[BaseExtractor] = []
    
    @classmethod
    def register(cls, extractor: BaseExtractor):
        """Register a new extractor"""
        cls._extractors.append(extractor)
    
    @classmethod
    def get_extractor(cls, url: str) -> Optional[BaseExtractor]:
        """Get the appropriate extractor for the given URL"""
        for extractor in cls._extractors:
            if extractor.can_handle(url):
                return extractor
        return None
    
    @classmethod
    def get_content_type(cls, url: str) -> Optional[ContentType]:
        """Get the content type for the given URL"""
        extractor = cls.get_extractor(url)
        return extractor.content_type if extractor else None