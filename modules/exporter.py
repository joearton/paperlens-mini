"""
Exporter Module for Sintesa
Export data to various formats
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from fpdf import FPDF
import json
import os
import platform
import subprocess


class Exporter:
    """Export research data to different formats"""
    
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export_to_csv(self, papers: List[Dict], filename: str = None) -> str:
        """Export papers to CSV file with improved structure"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"papers_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        # Create DataFrame
        df = pd.DataFrame(papers)
        
        # Reorder columns for better readability
        preferred_columns = ['title', 'authors', 'publication_date', 'year', 
                           'journal', 'citations', 'source', 'doi', 'url', 'abstract']
        
        # Extract year if not present
        if 'year' not in df.columns and 'publication_date' in df.columns:
            df['year'] = df['publication_date'].apply(self._extract_year)
        
        # Clean authors field - convert list to string
        if 'authors' in df.columns:
            df['authors'] = df['authors'].apply(
                lambda x: '; '.join(x) if isinstance(x, list) else str(x)
            )
        
        # Ensure all preferred columns exist
        available_columns = [col for col in preferred_columns if col in df.columns]
        other_columns = [col for col in df.columns if col not in preferred_columns]
        
        # Reorder
        df = df[available_columns + other_columns]
        
        # Sort by citations (descending)
        if 'citations' in df.columns:
            df = df.sort_values('citations', ascending=False)
        
        # Add metadata header as comments
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            f.write(f"# Sintesa - Research Papers Export\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total Papers: {len(papers)}\n")
            f.write(f"# Total Citations: {sum(p.get('citations', 0) for p in papers)}\n")
            f.write(f"# \n")
            
            # Write the actual CSV data
            df.to_csv(f, index=False)
        
        print(f"[OK] Exported to CSV: {filepath}")
        return str(filepath)
    
    def export_to_excel(self, papers: List[Dict], filename: str = None) -> str:
        """Export papers to Excel file with multiple sheets and analysis"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"papers_{timestamp}.xlsx"
        
        filepath = self.output_dir / filename
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 1. Summary Sheet
            total_papers = len(papers)
            total_citations = sum(p.get('citations', 0) for p in papers)
            avg_citations = total_citations / total_papers if total_papers > 0 else 0
            
            # Extract years
            years = [self._extract_year(p.get('publication_date')) for p in papers]
            years = [y for y in years if y is not None]
            year_range = f"{min(years)} - {max(years)}" if years else "N/A"
            
            summary_data = {
                'Metric': [
                    'Total Papers',
                    'Total Citations',
                    'Average Citations per Paper',
                    'Median Citations',
                    'Max Citations',
                    'Year Range',
                    'Unique Sources',
                    'Papers with DOI',
                    'Papers with Abstract',
                    'Generated Date'
                ],
                'Value': [
                    total_papers,
                    total_citations,
                    f'{avg_citations:.2f}',
                    pd.DataFrame(papers)['citations'].median(),
                    max((p.get('citations', 0) for p in papers), default=0),
                    year_range,
                    len(set(p.get('source', '') for p in papers)),
                    sum(1 for p in papers if p.get('doi')),
                    sum(1 for p in papers if p.get('abstract')),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # 2. All Papers Sheet
            df_papers = pd.DataFrame(papers)
            # Reorder columns for better readability
            preferred_columns = ['title', 'authors', 'publication_date', 'journal', 
                               'citations', 'source', 'doi', 'url', 'abstract']
            available_columns = [col for col in preferred_columns if col in df_papers.columns]
            other_columns = [col for col in df_papers.columns if col not in preferred_columns]
            df_papers = df_papers[available_columns + other_columns]
            df_papers.to_excel(writer, sheet_name='All Papers', index=False)
            
            # 3. Top Cited Papers
            top_papers = sorted(papers, key=lambda x: x.get('citations', 0), reverse=True)[:20]
            df_top = pd.DataFrame(top_papers)
            if not df_top.empty:
                df_top = df_top[available_columns]
            df_top.to_excel(writer, sheet_name='Top 20 Cited', index=False)
            
            # 4. Papers by Year
            if years:
                from collections import Counter
                year_counts = Counter(years)
                df_years = pd.DataFrame([
                    {'Year': year, 'Count': count, 'Percentage': f'{(count/len(years)*100):.1f}%'}
                    for year, count in sorted(year_counts.items(), reverse=True)
                ])
                df_years.to_excel(writer, sheet_name='By Year', index=False)
            
            # 5. Papers by Source
            df_source = pd.DataFrame(papers)
            if 'source' in df_source.columns:
                source_stats = df_source.groupby('source').agg({
                    'title': 'count',
                    'citations': ['sum', 'mean', 'median', 'max']
                }).round(2)
                source_stats.columns = ['Paper Count', 'Total Citations', 
                                       'Avg Citations', 'Median Citations', 'Max Citations']
                source_stats = source_stats.reset_index()
                source_stats.to_excel(writer, sheet_name='By Source', index=False)
            
            # 6. Authors Analysis (Top 20 most frequent authors)
            all_authors = []
            for paper in papers:
                authors = paper.get('authors', [])
                if isinstance(authors, list):
                    all_authors.extend(authors)
            
            if all_authors:
                from collections import Counter
                author_counts = Counter(all_authors).most_common(20)
                df_authors = pd.DataFrame(author_counts, columns=['Author', 'Paper Count'])
                df_authors.to_excel(writer, sheet_name='Top Authors', index=False)
            
            # 7. Journal Analysis (Top 20 journals)
            journals = [p.get('journal', 'N/A') for p in papers if p.get('journal')]
            if journals:
                from collections import Counter
                journal_counts = Counter(journals).most_common(20)
                df_journals = pd.DataFrame(journal_counts, columns=['Journal', 'Paper Count'])
                df_journals.to_excel(writer, sheet_name='Top Journals', index=False)
            
            # Format the worksheets
            workbook = writer.book
            
            # Format Summary sheet
            summary_sheet = workbook['Summary']
            summary_sheet.column_dimensions['A'].width = 30
            summary_sheet.column_dimensions['B'].width = 30
            
            # Format All Papers sheet
            papers_sheet = workbook['All Papers']
            papers_sheet.column_dimensions['A'].width = 50  # Title
            papers_sheet.column_dimensions['B'].width = 40  # Authors
            papers_sheet.column_dimensions['C'].width = 15  # Date
            papers_sheet.column_dimensions['D'].width = 30  # Journal
        
        print(f"[OK] Exported to Excel: {filepath}")
        return str(filepath)
    
    def export_to_json(self, papers: List[Dict], filename: str = None) -> str:
        """Export papers to JSON file with comprehensive metadata"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"papers_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Calculate statistics
        total_papers = len(papers)
        total_citations = sum(p.get('citations', 0) for p in papers)
        avg_citations = total_citations / total_papers if total_papers > 0 else 0
        
        # Extract years
        years = [self._extract_year(p.get('publication_date')) for p in papers]
        years = [y for y in years if y is not None]
        
        # Source distribution
        from collections import Counter
        sources = Counter(p.get('source', 'Unknown') for p in papers)
        
        # Top cited papers
        top_papers = sorted(papers, key=lambda x: x.get('citations', 0), reverse=True)[:10]
        top_cited_titles = [
            {
                'title': p.get('title', 'N/A'),
                'citations': p.get('citations', 0),
                'year': self._extract_year(p.get('publication_date'))
            }
            for p in top_papers
        ]
        
        # Authors statistics
        all_authors = []
        for paper in papers:
            authors = paper.get('authors', [])
            if isinstance(authors, list):
                all_authors.extend(authors)
        
        top_authors = Counter(all_authors).most_common(10) if all_authors else []
        
        export_data = {
            'metadata': {
                'application': 'Sintesa',
                'version': '1.0.0',
                'generated_at': datetime.now().isoformat(),
                'generated_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'export_format': 'JSON',
                'data_sources': list(sources.keys())
            },
            'statistics': {
                'total_papers': total_papers,
                'total_citations': total_citations,
                'average_citations': round(avg_citations, 2),
                'median_citations': int(pd.DataFrame(papers)['citations'].median()) if papers else 0,
                'max_citations': max((p.get('citations', 0) for p in papers), default=0),
                'year_range': {
                    'min': min(years) if years else None,
                    'max': max(years) if years else None,
                    'span': f"{min(years)}-{max(years)}" if years else None
                },
                'papers_by_source': dict(sources),
                'unique_sources': len(sources),
                'papers_with_doi': sum(1 for p in papers if p.get('doi')),
                'papers_with_abstract': sum(1 for p in papers if p.get('abstract')),
                'papers_with_url': sum(1 for p in papers if p.get('url'))
            },
            'top_cited_papers': top_cited_titles,
            'top_authors': [
                {'author': author, 'paper_count': count}
                for author, count in top_authors
            ],
            'year_distribution': dict(Counter(years)) if years else {},
            'papers': papers
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Exported to JSON: {filepath}")
        return str(filepath)
    
    def export_to_pdf(self, papers: List[Dict], filename: str = None) -> str:
        """Export papers to PDF report with comprehensive statistics"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.pdf"
        
        filepath = self.output_dir / filename
        
        pdf = PDF()
        pdf.add_page()
        
        # Title Page
        pdf.safe_set_font('Arial', 'B', 24)
        pdf.safe_cell(0, 20, 'Sintesa', 0, 1, 'C')
        pdf.safe_set_font('Arial', 'B', 18)
        pdf.safe_cell(0, 10, 'Research Paper Analysis Report', 0, 1, 'C')
        pdf.ln(10)
        
        # Date and metadata
        pdf.safe_set_font('Arial', '', 12)
        pdf.safe_cell(0, 8, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        pdf.safe_cell(0, 8, f'Total Papers Analyzed: {len(papers)}', 0, 1, 'C')
        pdf.ln(15)
        
        # Executive Summary Box
        pdf.set_fill_color(240, 248, 255)
        pdf.safe_set_font('Arial', 'B', 14)
        pdf.safe_cell(0, 10, 'Executive Summary', 0, 1, 'L', True)
        pdf.safe_set_font('Arial', '', 11)
        
        total_papers = len(papers)
        total_citations = sum(p.get('citations', 0) for p in papers)
        avg_citations = total_citations / total_papers if total_papers > 0 else 0
        
        # Calculate additional statistics
        df = pd.DataFrame(papers)
        sources = df['source'].value_counts().to_dict()
        
        # Year statistics
        years = [self._extract_year(p.get('publication_date')) for p in papers]
        years = [y for y in years if y is not None]
        year_range = f"{min(years)} - {max(years)}" if years else "N/A"
        
        # Top cited papers
        top_papers = sorted(papers, key=lambda x: x.get('citations', 0), reverse=True)[:5]
        
        pdf.safe_cell(0, 7, f'Total Papers: {total_papers}', 0, 1)
        pdf.safe_cell(0, 7, f'Total Citations: {total_citations:,}', 0, 1)
        pdf.safe_cell(0, 7, f'Average Citations per Paper: {avg_citations:.2f}', 0, 1)
        pdf.safe_cell(0, 7, f'Year Range: {year_range}', 0, 1)
        pdf.ln(5)
        
        # Source breakdown
        pdf.safe_set_font('Arial', 'B', 12)
        pdf.safe_cell(0, 7, 'Papers by Source:', 0, 1)
        pdf.safe_set_font('Arial', '', 11)
        for source, count in sources.items():
            percentage = (count / total_papers) * 100
            pdf.safe_cell(0, 6, f'  - {source}: {count} papers ({percentage:.1f}%)', 0, 1)
        pdf.ln(10)
        
        # Top 10 Most Cited Papers
        pdf.add_page()
        pdf.safe_set_font('Arial', 'B', 16)
        pdf.safe_cell(0, 10, '1. Top 10 Most Cited Papers', 0, 1)
        pdf.ln(3)
        
        for i, paper in enumerate(top_papers[:10], 1):
            pdf.safe_set_font('Arial', 'B', 11)
            title = paper.get('title', 'N/A')[:100]
            pdf.safe_multi_cell(0, 6, f'{i}. {title}')
            
            pdf.safe_set_font('Arial', '', 10)
            authors = ', '.join(paper.get('authors', [])[:3])
            if len(paper.get('authors', [])) > 3:
                authors += ' et al.'
            pdf.safe_cell(0, 5, f'   Authors: {authors}', 0, 1)
            
            year = paper.get('publication_date', 'N/A')
            citations = paper.get('citations', 0)
            source = paper.get('source', 'N/A')
            journal = paper.get('journal', 'N/A')
            pdf.safe_cell(0, 5, f'   Journal: {journal[:50]}', 0, 1)
            pdf.safe_cell(0, 5, f'   Year: {year}  |  Citations: {citations:,}  |  Source: {source}', 0, 1)
            
            if paper.get('doi'):
                pdf.safe_set_font('Arial', '', 9)
                pdf.safe_cell(0, 5, f'   DOI: {paper["doi"]}', 0, 1)
            
            pdf.ln(3)
        
        # Year Distribution Statistics
        pdf.add_page()
        pdf.safe_set_font('Arial', 'B', 16)
        pdf.safe_cell(0, 10, '2. Publications by Year', 0, 1)
        pdf.ln(3)
        
        if years:
            from collections import Counter
            year_counts = Counter(years)
            pdf.safe_set_font('Arial', '', 11)
            
            for year in sorted(year_counts.keys(), reverse=True):
                count = year_counts[year]
                percentage = (count / len(years)) * 100
                pdf.safe_cell(0, 6, f'{year}: {count} papers ({percentage:.1f}%)', 0, 1)
        else:
            pdf.safe_set_font('Arial', '', 11)
            pdf.safe_cell(0, 6, 'No year data available', 0, 1)
        
        pdf.ln(10)
        
        # Full Papers List
        pdf.add_page()
        pdf.safe_set_font('Arial', 'B', 16)
        pdf.safe_cell(0, 10, '3. Complete Papers List', 0, 1)
        pdf.ln(5)
        
        for i, paper in enumerate(papers[:100], 1):  # Limit to 100 papers
            pdf.safe_set_font('Arial', 'B', 10)
            title = paper.get('title', 'N/A')[:120]
            pdf.safe_multi_cell(0, 5, f'{i}. {title}')
            
            pdf.safe_set_font('Arial', '', 9)
            authors = ', '.join(paper.get('authors', [])[:4])
            if len(paper.get('authors', [])) > 4:
                authors += ' et al.'
            pdf.safe_cell(0, 4, f'   Authors: {authors[:100]}', 0, 1)
            
            year = paper.get('publication_date', 'N/A')
            citations = paper.get('citations', 0)
            source = paper.get('source', 'N/A')
            pdf.safe_cell(0, 4, f'   Year: {year}  |  Citations: {citations}  |  Source: {source}', 0, 1)
            pdf.ln(2)
            
            # Add new page every 12 papers
            if i % 12 == 0 and i < len(papers):
                pdf.add_page()
        
        # Footer page
        pdf.add_page()
        pdf.safe_set_font('Arial', 'B', 14)
        pdf.safe_cell(0, 10, 'About This Report', 0, 1)
        pdf.safe_set_font('Arial', '', 10)
        pdf.ln(3)
        
        pdf.safe_multi_cell(0, 5, 'This report was generated by Sintesa v1.0.0, a lightweight research paper analysis tool.')
        pdf.ln(3)
        pdf.safe_multi_cell(0, 5, 'Data Sources: CrossRef API, arXiv API')
        pdf.ln(3)
        pdf.safe_multi_cell(0, 5, 'Note: Citation counts may vary depending on the source database and update frequency.')
        pdf.ln(5)
        pdf.safe_set_font('Arial', 'I', 9)
        pdf.safe_multi_cell(0, 5, 'Disclaimer: This software is provided "as is" without warranty of any kind. The data accuracy depends on external sources.')
        
        pdf.output(str(filepath))
        
        print(f"[OK] Exported to PDF: {filepath}")
        return str(filepath)
    
    def open_file_manager(self, filepath: str) -> bool:
        """Open file manager to the exported file location"""
        try:
            filepath = Path(filepath)
            system = platform.system().lower()
            
            if system == 'darwin':  # macOS
                subprocess.run(['open', '-R', str(filepath)], check=True)
            elif system == 'windows':
                subprocess.run(['explorer', '/select,', str(filepath)], check=True)
            elif system == 'linux':
                # Try different file managers
                file_managers = ['nautilus', 'dolphin', 'thunar', 'pcmanfm', 'nemo']
                for manager in file_managers:
                    try:
                        subprocess.run([manager, '--select', str(filepath)], check=True)
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                else:
                    # Fallback: open parent directory
                    subprocess.run(['xdg-open', str(filepath.parent)], check=True)
            else:
                print(f"[FileManager] Unsupported OS: {system}")
                return False
            
            print(f"[FileManager] Opened file manager for: {filepath}")
            return True
            
        except Exception as e:
            print(f"[FileManager] Error opening file manager: {e}")
            return False
    
    def open_file(self, filepath: str) -> bool:
        """Open the exported file directly with default application"""
        try:
            filepath = Path(filepath)
            system = platform.system().lower()
            
            if system == 'darwin':  # macOS
                subprocess.run(['open', str(filepath)], check=True)
            elif system == 'windows':
                os.startfile(str(filepath))
            elif system == 'linux':
                subprocess.run(['xdg-open', str(filepath)], check=True)
            else:
                print(f"[FileOpen] Unsupported OS: {system}")
                return False
            
            print(f"[FileOpen] Opened file: {filepath}")
            return True
            
        except Exception as e:
            print(f"[FileOpen] Error opening file: {e}")
            return False
    
    def _extract_year(self, date_str) -> int:
        """Extract year from date string"""
        if not date_str or pd.isna(date_str):
            return None
        
        try:
            date_str = str(date_str)
            if '-' in date_str:
                parts = date_str.split('-')
                if parts[0].isdigit() and len(parts[0]) == 4:
                    return int(parts[0])
            elif '/' in date_str:
                parts = date_str.split('/')
                if parts[0].isdigit() and len(parts[0]) == 4:
                    return int(parts[0])
            elif date_str.isdigit() and len(date_str) == 4:
                return int(date_str)
            else:
                import re
                year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
                if year_match:
                    return int(year_match.group())
        except (ValueError, IndexError, AttributeError):
            pass
        
        return None


class PDF(FPDF):
    """Custom PDF class with header and footer and Unicode support"""
    
    def __init__(self):
        super().__init__()
        self.unicode_font = 'Arial'  # Use Arial as default since it's built-in
        self.fallback_font = 'Arial'
        
        # Try to add DejaVu font for Unicode support
        try:
            # Check if DejaVu fonts are available in common locations
            import os
            font_paths = [
                '/System/Library/Fonts/DejaVuSans.ttf',  # macOS
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
                'C:\\Windows\\Fonts\\DejaVuSans.ttf',  # Windows
                './fonts/DejaVuSans.ttf',  # Local fonts directory
            ]
            
            dejavu_found = False
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font_dir = os.path.dirname(font_path)
                    self.add_font('DejaVu', '', os.path.join(font_dir, 'DejaVuSans.ttf'), uni=True)
                    self.add_font('DejaVu', 'B', os.path.join(font_dir, 'DejaVuSans-Bold.ttf'), uni=True)
                    self.add_font('DejaVu', 'I', os.path.join(font_dir, 'DejaVuSans-Oblique.ttf'), uni=True)
                    self.add_font('DejaVu', 'BI', os.path.join(font_dir, 'DejaVuSans-BoldOblique.ttf'), uni=True)
                    self.unicode_font = 'DejaVu'
                    dejavu_found = True
                    print("[PDF] DejaVu fonts loaded successfully")
                    break
            
            if not dejavu_found:
                print("[PDF] DejaVu fonts not found, using Arial with character replacement")
                
        except Exception as e:
            print(f"[PDF] DejaVu fonts not available, using Arial with character replacement: {e}")
            self.unicode_font = 'Arial'
    
    def safe_set_font(self, family, style='', size=12):
        """Set font with fallback for Unicode characters"""
        try:
            # Always use Arial since it's built-in and reliable
            self.set_font('Arial', style, size)
        except Exception as e:
            print(f"[PDF] Font error, using fallback: {e}")
            # Last resort: use default font
            self.set_font('', style, size)
    
    def safe_multi_cell(self, w, h, txt, border=0, align='J', fill=False):
        """Multi-cell with Unicode character handling"""
        try:
            # Clean text to remove problematic characters
            clean_txt = self._clean_text(txt)
            self.multi_cell(w, h, clean_txt, border, align, fill)
        except Exception as e:
            print(f"[PDF] Text rendering error: {e}")
            # Fallback: replace problematic characters
            fallback_txt = self._replace_problematic_chars(txt)
            self.multi_cell(w, h, fallback_txt, border, align, fill)
    
    def safe_cell(self, w, h, txt, border=0, ln=0, align='', fill=False):
        """Cell with Unicode character handling"""
        try:
            clean_txt = self._clean_text(txt)
            self.cell(w, h, clean_txt, border, ln, align, fill)
        except Exception as e:
            print(f"[PDF] Text rendering error: {e}")
            fallback_txt = self._replace_problematic_chars(txt)
            self.cell(w, h, fallback_txt, border, ln, align, fill)
    
    def _clean_text(self, text):
        """Clean text for PDF rendering"""
        if not text:
            return text
        
        # Replace common problematic characters
        replacements = {
            ''': "'",
            ''': "'",
            '"': '"',
            '"': '"',
            '–': '-',
            '—': '-',
            '…': '...',
            '°': ' degrees',
            '±': '+/-',
            '×': 'x',
            '÷': '/',
            '≤': '<=',
            '≥': '>=',
            '≠': '!=',
            '≈': '~',
            '∞': 'infinity',
            'α': 'alpha',
            'β': 'beta',
            'γ': 'gamma',
            'δ': 'delta',
            'ε': 'epsilon',
            'θ': 'theta',
            'λ': 'lambda',
            'μ': 'mu',
            'π': 'pi',
            'σ': 'sigma',
            'τ': 'tau',
            'φ': 'phi',
            'χ': 'chi',
            'ψ': 'psi',
            'ω': 'omega'
        }
        
        result = str(text)
        for unicode_char, replacement in replacements.items():
            result = result.replace(unicode_char, replacement)
        
        return result
    
    def _replace_problematic_chars(self, text):
        """Replace all non-ASCII characters with safe alternatives"""
        if not text:
            return text
        
        result = str(text)
        # Replace any remaining non-ASCII characters with '?'
        result = ''.join(char if ord(char) < 128 else '?' for char in result)
        return result
    
    def header(self):
        """Add header to each page"""
        if self.page_no() > 1:
            self.safe_set_font('Arial', 'I', 10)
            self.safe_cell(0, 10, 'Sintesa Report', 0, 0, 'L')
            self.safe_cell(0, 10, f'Page {self.page_no()}', 0, 1, 'R')
            self.ln(5)
    
    def footer(self):
        """Add footer to each page"""
        self.set_y(-15)
        self.safe_set_font('Arial', 'I', 8)
        self.safe_cell(0, 10, 'Generated by Sintesa', 0, 0, 'C')

