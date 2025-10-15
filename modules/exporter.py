"""
Exporter Module for PaperLens Mini
Export data to various formats
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from fpdf import FPDF
import json


class Exporter:
    """Export research data to different formats"""
    
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export_to_csv(self, papers: List[Dict], filename: str = None) -> str:
        """Export papers to CSV file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"papers_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        df = pd.DataFrame(papers)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        print(f"[OK] Exported to CSV: {filepath}")
        return str(filepath)
    
    def export_to_excel(self, papers: List[Dict], filename: str = None) -> str:
        """Export papers to Excel file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"papers_{timestamp}.xlsx"
        
        filepath = self.output_dir / filename
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Papers sheet
            df_papers = pd.DataFrame(papers)
            df_papers.to_excel(writer, sheet_name='Papers', index=False)
            
            # Summary statistics
            summary_data = {
                'Total Papers': len(papers),
                'Total Citations': sum(p.get('citations', 0) for p in papers),
                'Average Citations': sum(p.get('citations', 0) for p in papers) / len(papers) if papers else 0,
                'Unique Sources': len(set(p.get('source', '') for p in papers))
            }
            df_summary = pd.DataFrame([summary_data])
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"[OK] Exported to Excel: {filepath}")
        return str(filepath)
    
    def export_to_json(self, papers: List[Dict], filename: str = None) -> str:
        """Export papers to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"papers_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_papers': len(papers)
            },
            'papers': papers
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Exported to JSON: {filepath}")
        return str(filepath)
    
    def export_to_pdf(self, papers: List[Dict], filename: str = None) -> str:
        """Export papers to PDF report"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.pdf"
        
        filepath = self.output_dir / filename
        
        pdf = PDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(0, 10, 'Research Paper Report', 0, 1, 'C')
        pdf.ln(5)
        
        # Date
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        pdf.ln(10)
        
        # Summary statistics
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, '1. Summary Statistics', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.ln(3)
        
        total_papers = len(papers)
        total_citations = sum(p.get('citations', 0) for p in papers)
        avg_citations = total_citations / total_papers if total_papers > 0 else 0
        
        pdf.cell(0, 8, f'Total Papers: {total_papers}', 0, 1)
        pdf.cell(0, 8, f'Total Citations: {total_citations:,}', 0, 1)
        pdf.cell(0, 8, f'Average Citations: {avg_citations:.2f}', 0, 1)
        pdf.ln(10)
        
        # Papers list
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, '2. Papers', 0, 1)
        pdf.ln(5)
        
        for i, paper in enumerate(papers[:50], 1):  # Limit to 50 papers
            pdf.set_font('Arial', 'B', 11)
            title = paper.get('title', 'N/A')[:100]  # Limit title length
            pdf.multi_cell(0, 6, f'{i}. {title}')
            
            pdf.set_font('Arial', '', 10)
            authors = ', '.join(paper.get('authors', [])[:3])  # Limit to 3 authors
            if len(paper.get('authors', [])) > 3:
                authors += ' et al.'
            pdf.cell(0, 5, f'   Authors: {authors}', 0, 1)
            
            year = paper.get('publication_date', 'N/A')
            citations = paper.get('citations', 0)
            source = paper.get('source', 'N/A')
            pdf.cell(0, 5, f'   Year: {year}  |  Citations: {citations}  |  Source: {source}', 0, 1)
            pdf.ln(3)
            
            # Add new page every 10 papers
            if i % 10 == 0 and i < len(papers):
                pdf.add_page()
        
        pdf.output(str(filepath))
        
        print(f"[OK] Exported to PDF: {filepath}")
        return str(filepath)


class PDF(FPDF):
    """Custom PDF class with header and footer"""
    
    def header(self):
        """Add header to each page"""
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, 'PaperLens Mini Report', 0, 0, 'L')
            self.cell(0, 10, f'Page {self.page_no()}', 0, 1, 'R')
            self.ln(5)
    
    def footer(self):
        """Add footer to each page"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Generated by PaperLens Mini', 0, 0, 'C')

