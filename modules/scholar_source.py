"""
Google Scholar Data Source Implementation
Uses scholarly library for reliable access
"""

from typing import List, Dict, Optional, Any
import time

try:
    from scholarly import scholarly, ProxyGenerator
    SCHOLARLY_AVAILABLE = True
except ImportError:
    SCHOLARLY_AVAILABLE = False
    print("[Scholar] WARNING: 'scholarly' library not installed. Install with: pip install scholarly")

from .base_source import BaseSource, SearchResult


class ScholarSource(BaseSource):
    """Google Scholar source using scholarly library"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._setup_scholarly()
    
    def _setup_scholarly(self):
        """Setup scholarly with optional proxy"""
        if not SCHOLARLY_AVAILABLE:
            return
        
        try:
            # Optional: Setup free proxy to avoid rate limiting
            # Uncomment if experiencing rate limits:
            # pg = ProxyGenerator()
            # pg.FreeProxies()
            # scholarly.use_proxy(pg)
            pass
        except Exception as e:
            print(f"[Scholar] Warning: Could not setup proxy: {e}")
    
    @property
    def source_config(self) -> Dict[str, Any]:
        return {
            "name": "Google Scholar",
            "description": "Academic search with citation counts and comprehensive coverage",
            "enabled": True,  # Now enabled with scholarly library
            "max_results_per_request": 20,
            "delay_between_requests": 2,  # Reduced delay with scholarly
        }
    
    def search(self, query: str, max_results: int = 100, from_year: Optional[int] = None,
               search_type: str = 'all') -> List[SearchResult]:
        """
        Search Google Scholar using scholarly library.
        
        Args:
            query: Search query string
            max_results: Maximum number of results (Google Scholar limits to ~100 per search)
            from_year: Filter papers from this year onwards
            search_type: Type of search - 'all', 'title', 'author', 'journal', 'keywords'
        """
        if not SCHOLARLY_AVAILABLE:
            print("[Scholar] ERROR: 'scholarly' library not installed")
            print("[Scholar] Install with: pip install scholarly")
            return []
        
        if not self.is_enabled():
            print("[Scholar] Source is disabled")
            return []
        
        print(f"[Scholar] Searching for: {query} (type: {search_type})")
        print(f"[Scholar] Note: Google Scholar may take longer due to rate limiting")
        
        try:
            results = []
            
            # Build search query based on type
            search_query = self._build_scholar_query(query, search_type)
            
            # Limit max_results to reasonable number for Google Scholar
            max_results = min(max_results, 100)
            
            # Search using scholarly
            search_results = scholarly.search_pubs(search_query)
            
            count = 0
            for result in search_results:
                if count >= max_results:
                    break
                
                try:
                    # Parse the result
                    parsed_result = self._parse_scholar_result(result)
                    
                    if parsed_result:
                        # Apply year filter if specified
                        if from_year and parsed_result.publication_date:
                            try:
                                pub_year = int(parsed_result.publication_date.split('-')[0])
                                if pub_year < from_year:
                                    continue
                            except (ValueError, IndexError):
                                pass
                        
                        results.append(parsed_result)
                        count += 1
                        
                        # Progress indicator
                        if count % 10 == 0:
                            print(f"[Scholar] Progress: {count}/{max_results} papers")
                    
                    # Small delay to avoid rate limiting
                    if count < max_results:
                        time.sleep(0.5)
                        
                except Exception as e:
                    print(f"[Scholar] Error parsing result: {e}")
                    continue
            
            print(f"[Scholar] Found {len(results)} results")
            return results
            
        except Exception as e:
            print(f"[Scholar] Error: {e}")
            print(f"[Scholar] This may be due to rate limiting. Try again later or use fewer results.")
            return []
    
    def _build_scholar_query(self, query: str, search_type: str) -> str:
        """Build Google Scholar search query based on search type."""
        if search_type == 'title':
            return f'intitle:{query}'
        elif search_type == 'author':
            return f'author:{query}'
        elif search_type == 'journal':
            return f'source:{query}'
        elif search_type == 'keywords':
            return query
        else:  # 'all' or default
            return query
    
    def _parse_scholar_result(self, result: Dict[str, Any]) -> Optional[SearchResult]:
        """Parse a scholarly result into a SearchResult object."""
        try:
            # Extract basic info using scholarly's structure
            bib = result.get('bib', {})
            
            title = bib.get('title', '')
            if not title:
                return None
            
            # Extract authors
            authors = []
            author_str = bib.get('author', '')
            if author_str:
                if isinstance(author_str, list):
                    authors = author_str
                else:
                    authors = [a.strip() for a in author_str.split(' and ')]
            
            # Extract abstract
            abstract = bib.get('abstract', '')
            
            # Extract publication info
            journal = bib.get('venue', '') or bib.get('journal', '')
            
            # Extract publication year
            pub_year = bib.get('pub_year', '')
            publication_date = str(pub_year) if pub_year else None
            
            # Extract URL
            url = result.get('pub_url', '') or result.get('eprint_url', '')
            
            # Extract citation count
            citations = result.get('num_citations', 0)
            if citations is None:
                citations = 0
            
            return SearchResult(
                title=title,
                authors=authors,
                abstract=abstract,
                doi=None,  # Google Scholar doesn't always provide DOI
                url=url,
                publication_date=publication_date,
                journal=journal,
                citations=int(citations),
                source="Google Scholar",
                raw_data=result
            )
            
        except Exception as e:
            print(f"[Scholar] Error parsing result: {e}")
            return None

