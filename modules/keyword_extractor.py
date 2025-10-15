"""
Simple Keyword Extractor - Without NLP/AI
Uses word frequency from titles
"""

from typing import List, Dict
from collections import Counter
import re


class KeywordExtractor:
    """Simple keyword extraction using word frequency"""
    
    def __init__(self):
        # Common stop words to exclude
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'it', 'its', 'they', 'them', 'their', 'we', 'our',
            'you', 'your', 'he', 'she', 'him', 'her', 'using', 'based', 'study',
            'research', 'analysis', 'paper', 'review', 'new', 'novel', 'approach'
        }
    
    def extract_keywords(self, papers: List[Dict], top_n: int = 20) -> List[str]:
        """
        Extract top keywords from paper titles using word frequency.
        
        Args:
            papers: List of paper dictionaries with 'title' field
            top_n: Number of top keywords to return
            
        Returns:
            List of keywords
        """
        # Collect all words from titles
        all_words = []
        
        for paper in papers:
            title = paper.get('title', '')
            if title:
                # Clean and tokenize
                words = self._tokenize(title)
                all_words.extend(words)
        
        # Count word frequency
        word_freq = Counter(all_words)
        
        # Get top N keywords
        top_keywords = [word for word, count in word_freq.most_common(top_n)]
        
        return top_keywords
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize and clean text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters, keep only letters and spaces
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Filter: remove stop words and short words
        words = [
            word for word in words
            if word not in self.stop_words
            and len(word) > 3  # Minimum 4 characters
        ]
        
        return words

