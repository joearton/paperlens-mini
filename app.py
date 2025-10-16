"""
PaperLens Mini - Main Application
Simplified version without AI/ML models
"""

import webview
from pathlib import Path
from typing import Dict, List, Any
import json
import config

# Import modules
from modules.data_fetcher import DataFetcher
from modules.visualizer import Visualizer
from modules.exporter import Exporter
from modules.keyword_extractor import KeywordExtractor

# Application version
APP_VERSION = "1.0.0"


class API:
    """API class for communication between frontend and backend"""
    
    def __init__(self):
        self.current_papers = []
        
        # Initialize components
        self.data_fetcher = DataFetcher()
        self.visualizer = Visualizer()
        self.exporter = Exporter(str(config.EXPORTS_DIR))
        self.keyword_extractor = KeywordExtractor()
    
    def search_papers(self, params: Dict) -> Dict:
        """Search for academic papers"""
        try:
            query = params.get('query', '')
            source = params.get('source', 'all')
            max_results = params.get('max_results', 50)
            from_year = params.get('from_year')
            search_type = params.get('search_type', 'all')
            
            if not query:
                return {
                    'success': False,
                    'error': 'Query is required',
                    'papers': []
                }
            
            print(f"\n[API] Searching for: {query}")
            print(f"[API] Source: {source}, Type: {search_type}, Max: {max_results}, Year: {from_year}")
            
            # Search papers
            papers = self.data_fetcher.search(
                query=query,
                source=source,
                max_results=max_results,
                from_year=from_year,
                search_type=search_type
            )
            
            self.current_papers = papers
            
            return {
                'success': True,
                'papers': papers,
                'count': len(papers)
            }
            
        except Exception as e:
            print(f"[API] Error in search_papers: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e),
                'papers': []
            }
    
    def generate_visualizations(self, papers: List[Dict]) -> Dict:
        """Generate visualizations for papers"""
        try:
            if not papers:
                return {
                    'success': False,
                    'error': 'No papers to visualize',
                    'visualizations': {}
                }
            
            print(f"[API] Generating visualizations for {len(papers)} papers")
            
            visualizations = {}
            
            # Extract keywords for network
            print("[API] Extracting keywords...")
            keywords = self.keyword_extractor.extract_keywords(papers, top_n=20)
            print(f"[API] Extracted {len(keywords)} keywords: {keywords[:10]}")
            
            # Word cloud (full width first)
            viz_wordcloud = self.visualizer.create_wordcloud(papers)
            visualizations['wordcloud'] = viz_wordcloud
            print("[API] [OK] Word cloud created")
            
            # Keyword network (full width second)
            if keywords and len(keywords) >= 2:
                viz_network = self.visualizer.create_keyword_network(keywords, papers)
                visualizations['network'] = viz_network
                print("[API] [OK] Keyword network created")
            else:
                print("[API] ! Not enough keywords for network")
            
            # Publications per year
            viz_years = self.visualizer.plot_publications_per_year(papers)
            visualizations['years'] = viz_years
            
            # Citation distribution
            viz_citations = self.visualizer.plot_citations_distribution(papers)
            visualizations['citations'] = viz_citations
            
            # Timeline
            viz_timeline = self.visualizer.create_timeline_chart(papers)
            visualizations['timeline'] = viz_timeline
            
            # Source distribution
            viz_sources = self.visualizer.plot_source_distribution(papers)
            visualizations['sources'] = viz_sources
            
            return {
                'success': True,
                'visualizations': visualizations
            }
            
        except Exception as e:
            print(f"[API] Error generating visualizations: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e),
                'visualizations': {}
            }
    
    def get_paper_statistics(self, papers: List[Dict]) -> Dict:
        """Get statistics about the papers including author analysis"""
        try:
            if not papers:
                return {
                    'success': False,
                    'error': 'No papers to analyze',
                    'statistics': {}
                }
            
            print(f"[API] Analyzing statistics for {len(papers)} papers")
            
            # Basic statistics
            total_papers = len(papers)
            
            # Collect all authors
            all_authors = []
            years = []
            sources = set()
            
            for paper in papers:
                # Extract authors
                authors = paper.get('authors', [])
                if isinstance(authors, list):
                    for author in authors:
                        if isinstance(author, dict):
                            author_name = author.get('name', '').strip()
                            if author_name:
                                all_authors.append({
                                    'name': author_name,
                                    'affiliation': author.get('affiliation', ''),
                                    'paper_title': paper.get('title', '')
                                })
                
                # Extract year
                year = paper.get('year')
                if year and isinstance(year, (int, str)):
                    try:
                        year_int = int(str(year))
                        if 1900 <= year_int <= 2030:
                            years.append(year_int)
                    except (ValueError, TypeError):
                        pass
                
                # Extract source
                source = paper.get('source', '')
                if source:
                    sources.add(source)
            
            # Count unique authors
            unique_authors = {}
            for author in all_authors:
                name = author['name']
                if name not in unique_authors:
                    unique_authors[name] = {
                        'name': name,
                        'affiliation': author['affiliation'],
                        'paper_count': 0,
                        'papers': []
                    }
                unique_authors[name]['paper_count'] += 1
                unique_authors[name]['papers'].append(author['paper_title'])
            
            # Get top 5 authors
            top_authors = sorted(
                unique_authors.values(),
                key=lambda x: x['paper_count'],
                reverse=True
            )[:5]
            
            # Year range
            year_range = "-"
            if years:
                min_year = min(years)
                max_year = max(years)
                if min_year == max_year:
                    year_range = str(min_year)
                else:
                    year_range = f"{min_year}-{max_year}"
            
            statistics = {
                'total_papers': total_papers,
                'total_authors': len(unique_authors),
                'year_range': year_range,
                'data_sources': len(sources),
                'top_authors': top_authors
            }
            
            print(f"[API] [OK] Statistics calculated: {total_papers} papers, {len(unique_authors)} authors")
            
            return {
                'success': True,
                'statistics': statistics
            }
            
        except Exception as e:
            print(f"[API] Error in get_paper_statistics: {e}")
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e),
                'statistics': {}
            }
    
    def export_data(self, format: str, papers: List[Dict]) -> Dict:
        """Export data to various formats"""
        try:
            if not papers:
                return {
                    'success': False,
                    'error': 'No papers to export'
                }
            
            print(f"[API] Exporting to {format}")
            
            filepath = None
            
            if format == 'csv':
                filepath = self.exporter.export_to_csv(papers)
            elif format == 'excel':
                filepath = self.exporter.export_to_excel(papers)
            elif format == 'json':
                filepath = self.exporter.export_to_json(papers)
            elif format == 'pdf':
                filepath = self.exporter.export_to_pdf(papers)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported format: {format}'
                }
            
            return {
                'success': True,
                'filepath': filepath
            }
            
        except Exception as e:
            print(f"[API] Error exporting data: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }
    
    def open_file_manager(self, filepath: str) -> Dict:
        """Open file manager to show exported file"""
        try:
            success = self.exporter.open_file_manager(filepath)
            return {
                'success': success,
                'message': 'File manager opened' if success else 'Failed to open file manager'
            }
        except Exception as e:
            print(f"[API] Error opening file manager: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def open_file(self, filepath: str) -> Dict:
        """Open exported file directly with default application"""
        try:
            success = self.exporter.open_file(filepath)
            return {
                'success': success,
                'message': 'File opened successfully' if success else 'Failed to open file'
            }
        except Exception as e:
            print(f"[API] Error opening file: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_app_info(self) -> Dict:
        """Get application information including version"""
        try:
            return {
                'success': True,
                'app_info': {
                    'name': 'PaperLens Mini',
                    'version': APP_VERSION,
                    'description': 'Academic Paper Search and Analysis Tool',
                    'author': 'PaperLens Team'
                }
            }
        except Exception as e:
            print(f"[API] Error getting app info: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_source_info(self) -> Dict:
        """Get information about data sources"""
        try:
            info = self.data_fetcher.get_source_info()
            return {
                'success': True,
                'sources': info
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Main application entry point"""
    print("="*60)
    print("PaperLens Mini - Simple Research Paper Analyzer")
    print("="*60)
    print()
    
    # Initialize API
    api = API()
    
    # Get UI directory
    ui_dir = Path(__file__).parent / "ui"
    
    # Create window
    window = webview.create_window(
        'PaperLens Mini',
        str(ui_dir / "index.html"),
        js_api=api,
        width=1200,
        height=800,
        resizable=True,
        min_size=(1000, 600)
    )
    
    print("[App] Starting PaperLens Mini...")
    webview.start(debug=True)


if __name__ == '__main__':
    main()

