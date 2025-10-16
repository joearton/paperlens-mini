"""
Data Fetcher Module for Sintesa
Handles fetching papers from various academic sources
"""

from typing import List, Dict, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

from .crossref_source import CrossrefSource
from .arxiv_source import ArxivSource
from .scholar_source import ScholarSource


class DataFetcher:
    """Simple data fetcher for academic papers"""
    
    def __init__(self):
        self.sources = {
            'crossref': CrossrefSource(),
            'arxiv': ArxivSource(),
            'scholar': ScholarSource()
        }
    
    def search(self, query: str, source: str = 'all', max_results: int = 100, 
               from_year: Optional[int] = None, search_type: str = 'all') -> List[Dict[str, Any]]:
        """
        Search for academic papers.
        
        Args:
            query: Search query string
            source: Source to search ('all', 'crossref', 'arxiv', 'scholar')
            max_results: Maximum number of results
            from_year: Filter papers from this year onwards
            search_type: Type of search - 'all', 'title', 'author', 'journal', 'keywords'
            
        Returns:
            List of paper dictionaries
        """
        print(f"\n{'='*60}")
        print(f"Searching for: {query}")
        print(f"Source: {source} | Type: {search_type} | Max results: {max_results} | From year: {from_year or 'Any'}")
        print(f"{'='*60}\n")
        
        results = []
        
        if source == 'all':
            # Search all sources in parallel
            # Divide max_results among sources to avoid exceeding total limit
            num_sources = len(self.sources)
            max_per_source = max(1, max_results // num_sources)
            
            print(f"Dividing {max_results} results among {num_sources} sources ({max_per_source} per source)")
            
            with ThreadPoolExecutor(max_workers=2) as executor:
                future_to_source = {
                    executor.submit(self._search_source, src_name, query, max_per_source, from_year, search_type): src_name
                    for src_name in self.sources.keys()
                }
                
                for future in as_completed(future_to_source):
                    src_name = future_to_source[future]
                    try:
                        source_results = future.result()
                        results.extend(source_results)
                        print(f"[OK] {src_name}: {len(source_results)} papers")
                    except Exception as e:
                        print(f"[ERROR] {src_name}: Error - {e}")
        
        else:
            # Search specific source
            if source in self.sources:
                results = self._search_source(source, query, max_results, from_year, search_type)
                print(f"[OK] {source}: {len(results)} papers")
            else:
                print(f"[ERROR] Unknown source: {source}")
        
        # Remove duplicates
        unique_results = self._remove_duplicates(results)
        
        # Limit results to max_results if exceeded
        if len(unique_results) > max_results:
            unique_results = unique_results[:max_results]
            print(f"Limited results to {max_results} papers")
        
        print(f"\n{'='*60}")
        print(f"Total: {len(results)} papers (after deduplication: {len(unique_results)})")
        print(f"{'='*60}\n")
        
        return unique_results
    
    def _search_source(self, source_name: str, query: str, max_results: int, 
                       from_year: Optional[int], search_type: str = 'all') -> List[Dict[str, Any]]:
        """Search a single source."""
        try:
            source = self.sources[source_name]
            search_results = source.search(query, max_results, from_year, search_type)
            
            # Convert SearchResult objects to dictionaries
            papers = []
            for result in search_results:
                paper_dict = {
                    'title': result.title or '',
                    'authors': result.authors or [],
                    'abstract': result.abstract or '',
                    'doi': result.doi or '',
                    'url': result.url or '',
                    'publication_date': result.publication_date or '',
                    'journal': result.journal or '',
                    'citations': int(result.citations) if result.citations else 0,
                    'source': result.source or '',
                }
                papers.append(paper_dict)
            
            return papers
            
        except Exception as e:
            print(f"Error searching {source_name}: {e}")
            return []
    
    def _remove_duplicates(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate papers based on title."""
        seen = set()
        unique_papers = []
        
        for paper in papers:
            title = paper.get('title', '').lower().strip()
            if title and title not in seen:
                seen.add(title)
                unique_papers.append(paper)
        
        return unique_papers
    
    def get_source_info(self) -> Dict[str, Any]:
        """Get information about all available sources."""
        source_info = {}
        for source_name, source in self.sources.items():
            source_info[source_name] = source.get_source_info()
        return source_info

