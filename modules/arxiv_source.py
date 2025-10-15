"""
arXiv Data Source Implementation
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Any

from .base_source import BaseSource, SearchResult


class ArxivSource(BaseSource):
    """arXiv data source implementation"""
    
    @property
    def source_config(self) -> Dict[str, Any]:
        return {
            "name": "arXiv",
            "description": "Open-access preprints in physics, math, CS, and more",
            "enabled": True,
            "max_results_per_request": 1000,
            "delay_between_requests": 3,
        }
    
    def search(self, query: str, max_results: int = 100, from_year: Optional[int] = None) -> List[SearchResult]:
        """Search arXiv for preprints and research papers."""
        if not self.is_enabled():
            return []
        
        print(f"[arXiv] Searching for: {query}")
        
        try:
            results = []
            start = 0
            
            while len(results) < max_results:
                url = "http://export.arxiv.org/api/query"
                params = {
                    'search_query': f'all:{query}',
                    'start': start,
                    'max_results': min(1000, max_results - len(results)),
                    'sortBy': 'relevance',
                    'sortOrder': 'descending'
                }
                
                try:
                    response = self.make_request(url, params)
                    root = ET.fromstring(response.content)
                    
                    entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
                    
                    for entry in entries:
                        result = self._parse_arxiv_entry(entry)
                        if result:
                            # Apply year filter if specified
                            if from_year and result.publication_date:
                                try:
                                    pub_year = int(result.publication_date.split('-')[0])
                                    if pub_year < from_year:
                                        continue
                                except (ValueError, IndexError):
                                    pass
                            
                            results.append(result)
                            if len(results) >= max_results:
                                break
                    
                    if len(entries) < 1000:
                        break
                        
                    start += len(entries)
                    self.delay_request()
                    
                except requests.exceptions.RequestException as e:
                    print(f"[arXiv] Error fetching results: {e}")
                    break
                    
            print(f"[arXiv] Found {len(results)} results")
            return results[:max_results]
            
        except Exception as e:
            print(f"[arXiv] Error: {e}")
            return []
    
    def _parse_arxiv_entry(self, entry: ET.Element) -> Optional[SearchResult]:
        """Parse an arXiv XML entry into a SearchResult object."""
        try:
            # Extract title
            title_elem = entry.find('.//{http://www.w3.org/2005/Atom}title')
            title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
            
            if not title:
                return None
            
            # Extract authors
            authors = []
            for author in entry.findall('.//{http://www.w3.org/2005/Atom}author'):
                name_elem = author.find('.//{http://www.w3.org/2005/Atom}name')
                if name_elem is not None and name_elem.text:
                    authors.append(name_elem.text.strip())
            
            # Extract abstract
            abstract_elem = entry.find('.//{http://www.w3.org/2005/Atom}summary')
            abstract = abstract_elem.text.strip() if abstract_elem is not None and abstract_elem.text else ""
            
            # Extract arXiv ID
            id_elem = entry.find('.//{http://www.w3.org/2005/Atom}id')
            arxiv_id = ""
            if id_elem is not None and id_elem.text:
                arxiv_id = id_elem.text.split('/')[-1]
            
            # Extract URL
            url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ""
            
            # Extract publication date
            published_elem = entry.find('.//{http://www.w3.org/2005/Atom}published')
            publication_date = None
            if published_elem is not None and published_elem.text:
                try:
                    date_str = published_elem.text
                    if 'T' in date_str:
                        publication_date = date_str.split('T')[0]
                except (ValueError, IndexError):
                    pass
            
            journal = "arXiv preprint"
            citations = 0
            
            return SearchResult(
                title=title,
                authors=authors,
                abstract=abstract,
                doi=None,
                url=url,
                publication_date=publication_date,
                journal=journal,
                citations=citations,
                source="arXiv",
                raw_data={'arxiv_id': arxiv_id}
            )
            
        except Exception as e:
            print(f"[arXiv] Error parsing entry: {e}")
            return None

