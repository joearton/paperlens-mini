"""
Visualizer Module for PaperLens Mini
Creates simple visualizations without AI/ML
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Optional, Union
import pandas as pd
import re
import numpy as np
import json
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    print("[Viz] NetworkX not available - keyword network will be disabled")

try:
    from wordcloud import WordCloud
    import io
    import base64
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    print("[Viz] WordCloud not available - wordcloud visualization will be disabled")


class Visualizer:
    """Create simple visualizations for research data"""
    
    def __init__(self):
        self.default_layout = {
            'template': 'plotly_white',
            'font': {'family': 'Arial, sans-serif', 'size': 12},
            'margin': {'l': 50, 'r': 50, 't': 80, 'b': 50},
        }
        
        self.colors = {
            'primary': '#3498db',
            'secondary': '#e74c3c',
            'success': '#2ecc71',
        }
    
    def plot_publications_per_year(self, papers: List[Dict]) -> str:
        """Create bar chart showing publications per year"""
        try:
            df = pd.DataFrame(papers)
            
            # Extract year from publication_date
            df['year'] = df['publication_date'].apply(self._extract_year)
            df = df.dropna(subset=['year'])
            
            if df.empty:
                return self._create_empty_chart("No valid year data")
            
            year_counts = df['year'].value_counts().sort_index()
            
            # Convert to lists to avoid binary encoding
            years = list(year_counts.index)
            counts = [int(c) for c in year_counts.values]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=years,
                    y=counts,
                    marker=dict(color=self.colors['primary']),
                    hovertemplate='<b>%{x}</b><br>Papers: %{y}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                **self.default_layout,
                title='Publications per Year',
                xaxis=dict(title='Year'),
                yaxis=dict(title='Number of Papers'),
                width=800,
                height=500
            )
            
            return fig.to_html(full_html=False, include_plotlyjs=False)
            
        except Exception as e:
            print(f"Error creating year chart: {e}")
            return self._create_empty_chart(f"Error: {e}")
    
    def plot_citations_distribution(self, papers: List[Dict]) -> str:
        """Create histogram showing citation distribution"""
        try:
            df = pd.DataFrame(papers)
            df['citations'] = pd.to_numeric(df['citations'], errors='coerce')
            df = df.dropna(subset=['citations'])
            
            if df.empty:
                return self._create_empty_chart("No valid citation data")
            
            # Check if all citations are 0
            if df['citations'].max() == 0:
                return self._create_info_chart(
                    "All papers have 0 citations",
                    f"Total Papers: {len(df)}<br>This is normal for papers from sources<br>that don't provide citation counts"
                )
            
            # Convert to list to avoid binary encoding
            citations = [int(c) for c in df['citations']]
            
            fig = go.Figure(data=[
                go.Histogram(
                    x=citations,
                    nbinsx=20,
                    marker=dict(color=self.colors['success']),
                    hovertemplate='Citations: %{x}<br>Count: %{y}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                **self.default_layout,
                title='Citation Distribution',
                xaxis=dict(title='Citations'),
                yaxis=dict(title='Number of Papers'),
                width=800,
                height=500
            )
            
            return fig.to_html(full_html=False, include_plotlyjs=False)
            
        except Exception as e:
            print(f"Error creating citation chart: {e}")
            return self._create_empty_chart(f"Error: {e}")
    
    def create_timeline_chart(self, papers: List[Dict]) -> str:
        """Create timeline scatter plot"""
        try:
            df = pd.DataFrame(papers)
            df['year'] = df['publication_date'].apply(self._extract_year)
            df['citations'] = pd.to_numeric(df['citations'], errors='coerce')
            df = df.dropna(subset=['year', 'citations'])
            
            if df.empty:
                return self._create_empty_chart("No valid timeline data")
            
            # Convert to lists to avoid binary encoding
            years = [int(y) for y in df['year']]
            citations = [int(c) for c in df['citations']]
            titles = list(df['title'])
            
            fig = go.Figure(data=[
                go.Scatter(
                    x=years,
                    y=citations,
                    mode='markers',
                    marker=dict(color=self.colors['primary'], size=8),
                    hovertemplate='<b>%{text}</b><br>Year: %{x}<br>Citations: %{y}<extra></extra>',
                    text=titles
                )
            ])
            
            fig.update_layout(
                **self.default_layout,
                title='Publication Timeline',
                xaxis_title='Year',
                yaxis_title='Citations',
                width=800,
                height=500
            )
            
            return fig.to_html(full_html=False, include_plotlyjs=False)
            
        except Exception as e:
            print(f"Error creating timeline: {e}")
            import traceback
            traceback.print_exc()
            return self._create_empty_chart(f"Error: {e}")
    
    def plot_source_distribution(self, papers: List[Dict]) -> str:
        """Create pie chart showing papers by source"""
        try:
            df = pd.DataFrame(papers)
            
            if 'source' not in df.columns or df.empty:
                return self._create_empty_chart("No source data available")
            
            source_counts = df['source'].value_counts()
            
            # Convert to lists to avoid binary encoding
            labels = list(source_counts.index)
            values = [int(v) for v in source_counts.values]
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hovertemplate='<b>%{label}</b><br>Papers: %{value}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                **self.default_layout,
                title='Papers by Source',
                width=800,
                height=500
            )
            
            return fig.to_html(full_html=False, include_plotlyjs=False)
            
        except Exception as e:
            print(f"Error creating source chart: {e}")
            return self._create_empty_chart(f"Error: {e}")
    
    def _extract_year(self, date_str) -> Optional[int]:
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
                year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
                if year_match:
                    return int(year_match.group())
        except (ValueError, IndexError, AttributeError):
            pass
        
        return None
    
    def _create_empty_chart(self, message: str) -> str:
        """Create empty chart with message"""
        fig = go.Figure()
        fig.add_annotation(
            text=f"<b>{message}</b>",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font_size=16
        )
        fig.update_layout(
            **self.default_layout,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            width=800,
            height=500
        )
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    def _create_info_chart(self, title: str, message: str) -> str:
        """Create informational chart"""
        fig = go.Figure()
        fig.add_annotation(
            text=f"<b>{title}</b><br><br>{message}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font_size=14,
            bgcolor='rgba(240,240,240,0.8)',
            borderwidth=2,
            bordercolor=self.colors['primary']
        )
        fig.update_layout(
            **self.default_layout,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            width=800,
            height=500
        )
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    def create_keyword_network(self, keywords: List[str], papers: List[Dict] = None) -> str:
        """
        Create keyword network visualization (simplified version without AI).
        
        Args:
            keywords: List of keywords to visualize
            papers: List of papers (optional, for co-occurrence)
            
        Returns:
            HTML string for the chart
        """
        if not NETWORKX_AVAILABLE:
            return self._create_empty_chart("NetworkX library not installed")
        
        try:
            if not keywords or len(keywords) < 2:
                return self._create_empty_chart("Need at least 2 keywords for network")
            
            # Limit to 25 keywords for better visualization
            keywords = keywords[:25]
            
            # Create graph
            G = nx.Graph()
            
            # Add nodes
            for keyword in keywords:
                G.add_node(keyword)
            
            # Add edges based on word co-occurrence in titles
            if papers:
                for i, kw1 in enumerate(keywords):
                    for j, kw2 in enumerate(keywords[i+1:], i+1):
                        # Check co-occurrence in titles
                        cooccur_count = 0
                        for paper in papers:
                            title = paper.get('title', '').lower()
                            if kw1.lower() in title and kw2.lower() in title:
                                cooccur_count += 1
                        
                        if cooccur_count > 0:
                            weight = cooccur_count / len(papers)
                            G.add_edge(kw1, kw2, weight=weight)
            else:
                # Fallback: connect based on word similarity
                for i, kw1 in enumerate(keywords):
                    for j, kw2 in enumerate(keywords[i+1:], i+1):
                        words1 = set(kw1.lower().split())
                        words2 = set(kw2.lower().split())
                        overlap = len(words1.intersection(words2))
                        if overlap > 0:
                            G.add_edge(kw1, kw2, weight=overlap / max(len(words1), len(words2)))
            
            # Ensure minimum connectivity
            if len(G.edges()) == 0:
                for i in range(len(keywords) - 1):
                    G.add_edge(keywords[i], keywords[i+1], weight=0.3)
            
            # Layout
            pos = nx.spring_layout(G, k=2, iterations=50)
            
            # Create edge trace
            edge_x = []
            edge_y = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
            
            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=1, color='#888'),
                hoverinfo='none',
                mode='lines'
            )
            
            # Create node trace
            node_x = []
            node_y = []
            node_text = []
            node_size = []
            
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(node)
                # Size based on degree
                degree = G.degree(node)
                node_size.append(20 + degree * 5)
            
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                text=node_text,
                textposition='middle center',
                marker=dict(
                    size=node_size,
                    color=self.colors['primary'],
                    line=dict(width=2, color='white')
                ),
                textfont=dict(size=10, color='#2c3e50'),
                hoverinfo='text',
                hovertext=node_text
            )
            
            # Create figure
            fig = go.Figure(data=[edge_trace, node_trace])
            
            fig.update_layout(
                **self.default_layout,
                title='Keyword Network',
                showlegend=False,
                hovermode='closest',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                width=900,
                height=600
            )
            
            return fig.to_html(full_html=False, include_plotlyjs=False)
            
        except Exception as e:
            print(f"Error creating keyword network: {e}")
            import traceback
            traceback.print_exc()
            return self._create_empty_chart(f"Error: {e}")
    
    def create_wordcloud(self, papers: List[Dict]) -> str:
        """
        Create word cloud visualization from paper titles and abstracts.
        
        Args:
            papers: List of papers to extract text from
            
        Returns:
            HTML string with embedded image
        """
        if not WORDCLOUD_AVAILABLE:
            return self._create_empty_chart("WordCloud library not installed")
        
        try:
            if not papers:
                return self._create_empty_chart("No papers available for word cloud")
            
            # Collect text from titles and abstracts
            text_data = []
            for paper in papers:
                if paper.get('title'):
                    text_data.append(paper['title'])
                if paper.get('abstract'):
                    # Limit abstract to first 200 chars to avoid dominance
                    abstract = paper['abstract'][:200]
                    text_data.append(abstract)
            
            if not text_data:
                return self._create_empty_chart("No text data available for word cloud")
            
            # Combine all text
            combined_text = ' '.join(text_data)
            
            # Common stopwords for academic papers
            stopwords = set([
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                'of', 'with', 'from', 'by', 'as', 'is', 'was', 'are', 'were', 'been',
                'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                'should', 'could', 'may', 'might', 'can', 'this', 'that', 'these',
                'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
                'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both',
                'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same',
                'so', 'than', 'too', 'very', 'also', 'however', 'therefore', 'thus',
                'furthermore', 'moreover', 'nevertheless', 'using', 'used', 'study',
                'paper', 'research', 'results', 'method', 'approach', 'based'
            ])
            
            # Generate word cloud
            wc = WordCloud(
                width=900,
                height=500,
                background_color='white',
                stopwords=stopwords,
                max_words=100,
                relative_scaling=0.5,
                colormap='viridis',
                min_font_size=10
            ).generate(combined_text)
            
            # Convert to image
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            ax.set_title('Word Cloud from Paper Titles & Abstracts', 
                        fontsize=16, fontweight='bold', pad=20)
            
            # Save to bytes
            buf = io.BytesIO()
            plt.tight_layout(pad=1)
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            plt.close(fig)
            buf.seek(0)
            
            # Encode to base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            
            # Create HTML with embedded image
            html = f'''
            <div style="text-align: center; padding: 20px;">
                <img src="data:image/png;base64,{img_base64}" 
                     style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"
                     alt="Word Cloud">
            </div>
            '''
            
            return html
            
        except Exception as e:
            print(f"Error creating word cloud: {e}")
            import traceback
            traceback.print_exc()
            return self._create_empty_chart(f"Error: {e}")

