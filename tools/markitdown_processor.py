"""
Multi-URL Markitdown Processor Tool

This module provides functionality to process multiple URLs using markitdown,
converting web content to markdown format. Follows clean code principles
with proper separation of concerns, error handling, and type safety.
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from urllib.parse import urlparse

from markitdown import MarkItDown
from ratelimit import limits, sleep_and_retry

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ProcessedDocument:
    """Represents a processed document with metadata."""
    url: str
    title: str
    text_content: str
    success: bool
    error_message: Optional[str] = None


@dataclass
class MarkitdownResult:
    """Container for markitdown processing results."""
    documents: List[ProcessedDocument]
    total_processed: int
    successful_count: int
    failed_count: int
    
    @property
    def success_rate(self) -> float:
        """Calculate the success rate as a percentage."""
        if self.total_processed == 0:
            return 0.0
        return (self.successful_count / self.total_processed) * 100


class URLValidator:
    """Validates URL format and accessibility."""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL has valid format."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def validate_urls(urls: List[str]) -> tuple[List[str], List[str]]:
        """Separate valid and invalid URLs."""
        valid_urls = []
        invalid_urls = []
        
        for url in urls:
            if URLValidator.is_valid_url(url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        return valid_urls, invalid_urls


class MarkitdownProcessor:
    """Processes multiple URLs using markitdown with rate limiting and error handling."""
    
    def __init__(self, max_workers: int = 5, timeout: int = 30):
        """
        Initialize the processor.
        
        Args:
            max_workers: Maximum number of concurrent workers
            timeout: Timeout for each URL processing in seconds
        """
        self.max_workers = max_workers
        self.timeout = timeout
        self._markitdown = MarkItDown()
    
    @limits(calls=10, period=60)  # Rate limit: 10 calls per minute
    @sleep_and_retry
    def _process_single_url(self, url: str) -> ProcessedDocument:
        """
        Process a single URL with rate limiting.
        
        Args:
            url: The URL to process
            
        Returns:
            ProcessedDocument: Processed document result
        """
        try:
            logger.info(f"Processing URL: {url}")
            result = self._markitdown.convert(url)
            
            return ProcessedDocument(
                url=url,
                title=getattr(result, 'title', url),
                text_content=result.text_content,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Failed to process {url}: {str(e)}")
            return ProcessedDocument(
                url=url,
                title="",
                text_content="",
                success=False,
                error_message=str(e)
            )
    
    def process_urls(self, urls: List[str]) -> MarkitdownResult:
        """
        Process multiple URLs concurrently.
        
        Args:
            urls: List of URLs to process
            
        Returns:
            MarkitdownResult: Collection of processed documents with metadata
            
        Raises:
            ValueError: If urls list is empty or contains only invalid URLs
        """
        if not urls:
            raise ValueError("URLs list cannot be empty")
        
        # Validate URLs
        valid_urls, invalid_urls = URLValidator.validate_urls(urls)
        
        if invalid_urls:
            logger.warning(f"Found {len(invalid_urls)} invalid URLs: {invalid_urls}")
        
        if not valid_urls:
            raise ValueError("No valid URLs provided")
        
        documents = []
        successful_count = 0
        
        # Process URLs concurrently
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all URL processing tasks
            future_to_url = {
                executor.submit(self._process_single_url, url): url 
                for url in valid_urls
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_url):
                try:
                    document = future.result(timeout=self.timeout)
                    documents.append(document)
                    
                    if document.success:
                        successful_count += 1
                        
                except Exception as e:
                    url = future_to_url[future]
                    logger.error(f"Unexpected error processing {url}: {str(e)}")
                    documents.append(ProcessedDocument(
                        url=url,
                        title="",
                        text_content="",
                        success=False,
                        error_message=f"Unexpected error: {str(e)}"
                    ))
        
        return MarkitdownResult(
            documents=documents,
            total_processed=len(documents),
            successful_count=successful_count,
            failed_count=len(documents) - successful_count
        )


# Public API function following the existing pattern
def process_multiple_urls(
    urls: Union[List[str], str], 
    max_workers: int = 5,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Process multiple URLs using markitdown to extract content as markdown.
    
    This function provides a clean interface for processing multiple web URLs
    and converting their content to markdown format using the markitdown library.
    
    Args:
        urls: Single URL string or list of URL strings to process
        max_workers: Maximum number of concurrent workers (default: 5)
        timeout: Timeout for each URL processing in seconds (default: 30)
        
    Returns:
        Dict containing:
        - 'documents': List of processed documents with content and metadata
        - 'summary': Processing summary statistics
        - 'success': Overall success boolean
        
    Example:
        >>> result = process_multiple_urls([
        ...     "https://example.com/article1",
        ...     "https://example.com/article2"
        ... ])
        >>> print(f"Processed {result['summary']['total_processed']} URLs")
        >>> for doc in result['documents']:
        ...     if doc['success']:
        ...         print(f"Title: {doc['title']}")
        ...         print(f"Content: {doc['content'][:100]}...")
    """
    # Normalize input to list
    if isinstance(urls, str):
        url_list = [urls]
    else:
        url_list = urls
    
    try:
        processor = MarkitdownProcessor(max_workers=max_workers, timeout=timeout)
        result = processor.process_urls(url_list)
        
        return {
            'documents': [
                {
                    'url': doc.url,
                    'title': doc.title,
                    'content': doc.text_content,
                    'success': doc.success,
                    'error_message': doc.error_message
                }
                for doc in result.documents
            ],
            'summary': {
                'total_processed': result.total_processed,
                'successful_count': result.successful_count,
                'failed_count': result.failed_count,
                'success_rate': result.success_rate
            },
            'success': result.successful_count > 0
        }
        
    except Exception as e:
        logger.error(f"Error in process_multiple_urls: {str(e)}")
        return {
            'documents': [],
            'summary': {
                'total_processed': 0,
                'successful_count': 0,
                'failed_count': len(url_list),
                'success_rate': 0.0
            },
            'success': False,
            'error': str(e)
        }