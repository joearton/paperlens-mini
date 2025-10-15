"""
Base Source Class for PaperLens Mini Data Sources
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
import time
import requests
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Data class for search results"""
    title: str
    authors: List[str]
    abstract: str
    doi: Optional[str]
    url: Optional[str]
    publication_date: Optional[str]
    journal: Optional[str]
    citations: Optional[int]
    source: str
    raw_data: Dict[str, Any]


class BaseSource(ABC):
    """
    Abstract base class for all data sources.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the data source with configuration."""
        self.config = config or {}
        self.source_name = self.__class__.__name__.lower().replace('source', '')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PaperLens-Mini/1.0 (Academic Research Tool)'
        })
    
    @property
    @abstractmethod
    def source_config(self) -> Dict[str, Any]:
        """Return the default configuration for this source."""
        pass
    
    @abstractmethod
    def search(self, query: str, max_results: int = 100, from_year: Optional[int] = None, 
               search_type: str = 'all') -> List[SearchResult]:
        """
        Search for papers in this data source.
        
        Args:
            query: Search query string
            max_results: Maximum number of results
            from_year: Filter papers from this year onwards
            search_type: Type of search - 'all', 'title', 'author', 'journal', 'keywords'
        """
        pass
    
    def is_enabled(self) -> bool:
        """Check if this source is enabled in configuration"""
        return self.config.get('enabled', self.source_config.get('enabled', True))
    
    def get_max_results_per_request(self) -> int:
        """Get maximum results per request from config"""
        return self.config.get(
            'max_results_per_request', 
            self.source_config.get('max_results_per_request', 100)
        )
    
    def get_delay_between_requests(self) -> float:
        """Get delay between requests from config"""
        return self.config.get(
            'delay_between_requests',
            self.source_config.get('delay_between_requests', 1.0)
        )
    
    def delay_request(self):
        """Apply delay between requests"""
        delay = self.get_delay_between_requests()
        if delay > 0:
            time.sleep(delay)
    
    def make_request(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Make HTTP request with error handling and rate limiting."""
        try:
            if headers:
                request_headers = self.session.headers.copy()
                request_headers.update(headers)
            else:
                request_headers = self.session.headers
            
            response = self.session.get(url, params=params, headers=request_headers, timeout=30)
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"Request error in {self.source_name}: {e}")
            raise
    
    def get_source_info(self) -> Dict[str, Any]:
        """Get information about this data source."""
        return {
            'name': self.source_config['name'],
            'description': self.source_config['description'],
            'enabled': self.is_enabled(),
            'max_results_per_request': self.get_max_results_per_request()
        }

