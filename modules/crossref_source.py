"""
CrossRef Data Source Implementation
"""

import requests
from typing import List, Dict, Optional, Any
import re

from .base_source import BaseSource, SearchResult


class CrossrefSource(BaseSource):
    """CrossRef data source implementation"""
    
    @property
    def source_config(self) -> Dict[str, Any]:
        return {
            "name": "CrossRef",
            "description": "Fast and reliable academic database with DOI links",
            "enabled": True,
            "max_results_per_request": 500,
            "delay_between_requests": 1.5,
        }
    
    def search(self, query: str, max_results: int = 100, from_year: Optional[int] = None,
               search_type: str = 'all') -> List[SearchResult]:
        """
        Search CrossRef for academic papers with advanced search options.
        
        Args:
            query: Search query string
            max_results: Maximum number of results
            from_year: Filter papers from this year onwards
            search_type: Type of search - 'all', 'title', 'author', 'journal', 'keywords'
        """
        if not self.is_enabled():
            return []
        
        print(f"[CrossRef] Searching for: {query} (type: {search_type})")
        
        try:
            results = []
            start = 0
            rows = min(max_results, self.get_max_results_per_request())
            
            while len(results) < max_results and start < 10000:
                url = "https://api.crossref.org/works"
                
                # Build query based on search type
                params = self._build_query_params(query, search_type, rows, start, max_results - len(results))
                
                if from_year:
                    existing_filter = params.get('filter', '')
                    if existing_filter:
                        params['filter'] = f'{existing_filter},from-pub-date:{from_year}'
                    else:
                        params['filter'] = f'from-pub-date:{from_year}'
                
                try:
                    response = self.make_request(url, params)
                    data = response.json()
                    
                    if 'message' in data and 'items' in data['message']:
                        for item in data['message']['items']:
                            result = self._parse_crossref_item(item)
                            if result:
                                results.append(result)
                    
                    if len(data.get('message', {}).get('items', [])) < rows:
                        break
                        
                    start += rows
                    self.delay_request()
                    
                except requests.exceptions.RequestException as e:
                    print(f"[CrossRef] Error fetching results: {e}")
                    break
                    
            print(f"[CrossRef] Found {len(results)} results")
            return results[:max_results]
            
        except Exception as e:
            print(f"[CrossRef] Error: {e}")
            return []
    
    def _build_query_params(self, query: str, search_type: str, rows: int, offset: int, 
                           max_remaining: int) -> Dict[str, Any]:
        """Build query parameters based on search type."""
        params = {
            'rows': min(rows, max_remaining),
            'offset': offset,
            'sort': 'relevance',
            'order': 'desc'
        }
        
        # CrossRef API supports field-specific queries
        if search_type == 'title':
            params['query.title'] = query
        elif search_type == 'author':
            params['query.author'] = query
        elif search_type == 'journal':
            params['query.container-title'] = query
        elif search_type == 'keywords':
            params['query'] = query
        else:  # 'all' or default
            params['query'] = query
        
        return params
    
    def _parse_crossref_item(self, item: Dict[str, Any]) -> Optional[SearchResult]:
        """Parse a CrossRef API item into a SearchResult object."""
        try:
            # Extract title
            title = ""
            if 'title' in item and item['title']:
                title = item['title'][0] if isinstance(item['title'], list) else str(item['title'])
            
            if not title:
                return None
            
            # Extract authors
            authors = []
            if 'author' in item and item['author']:
                for author in item['author']:
                    if 'given' in author and 'family' in author:
                        authors.append(f"{author['given']} {author['family']}")
                    elif 'name' in author:
                        authors.append(author['name'])
            
            # Extract abstract
            abstract = ""
            if 'abstract' in item and item['abstract']:
                abstract = re.sub(r'<[^>]+>', '', str(item['abstract'])).strip()
            
            # Extract DOI
            doi = item.get('DOI', '')
            
            # Extract URL
            url = item.get('URL', '')
            if not url and doi:
                url = f"https://doi.org/{doi}"
            
            # Extract publication date
            publication_date = None
            date_fields = ['published-print', 'published-online', 'issued']
            for field in date_fields:
                if field in item and 'date-parts' in item[field]:
                    date_parts = item[field]['date-parts'][0]
                    if len(date_parts) >= 3:
                        publication_date = f"{date_parts[0]}-{date_parts[1]:02d}-{date_parts[2]:02d}"
                    elif len(date_parts) >= 1:
                        publication_date = str(date_parts[0])
                    break
            
            # Extract journal
            journal = ""
            if 'container-title' in item and item['container-title']:
                journal = item['container-title'][0] if isinstance(item['container-title'], list) else str(item['container-title'])
            
            # Extract citation count
            citations = 0
            if 'is-referenced-by-count' in item:
                citations = item['is-referenced-by-count']
            
            return SearchResult(
                title=title,
                authors=authors,
                abstract=abstract,
                doi=doi,
                url=url,
                publication_date=publication_date,
                journal=journal,
                citations=citations,
                source="CrossRef",
                raw_data=item
            )
            
        except Exception as e:
            print(f"[CrossRef] Error parsing item: {e}")
            return None

