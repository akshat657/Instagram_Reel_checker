"""
Research paper fetcher for medical citations.
Fetches papers from PubMed, PMC, and Europe PMC in parallel.
"""

import requests
import time
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher


def fetch_pubmed_papers(query: str, limit: int = 4) -> List[Dict[str, Any]]:
    """
    Fetch papers from PubMed with abstracts.

    Args:
        query: Search query string
        limit: Maximum number of papers to fetch

    Returns:
        List of paper dicts with title, abstract, url, source, year, pmid
    """
    papers = []

    try:
        # Step 1: Search for PMIDs
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": limit,
            "retmode": "json"
        }

        search_response = requests.get(search_url, params=search_params, timeout=8)

        if search_response.status_code != 200:
            return []

        search_data = search_response.json()
        pmids = search_data.get('esearchresult', {}).get('idlist', [])

        if not pmids:
            return []

        # Step 2: Fetch paper details including abstracts
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml"
        }

        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=8)

        if fetch_response.status_code != 200:
            return []

        # Parse XML response
        import xml.etree.ElementTree as ET
        root = ET.fromstring(fetch_response.content)

        for article in root.findall('.//PubmedArticle'):
            try:
                # Extract title
                title_elem = article.find('.//ArticleTitle')
                title = title_elem.text if title_elem is not None else "No title"

                # Extract abstract
                abstract_parts = article.findall('.//AbstractText')
                abstract = " ".join([part.text for part in abstract_parts if part.text])
                if not abstract:
                    abstract = "Abstract not available"

                # Truncate abstract to 250 words
                abstract_words = abstract.split()
                if len(abstract_words) > 250:
                    abstract = " ".join(abstract_words[:250]) + "..."

                # Extract year
                year_elem = article.find('.//PubDate/Year')
                year = year_elem.text if year_elem is not None else "N/A"

                # Extract PMID
                pmid_elem = article.find('.//PMID')
                pmid = pmid_elem.text if pmid_elem is not None else ""

                papers.append({
                    "title": title,
                    "abstract": abstract,
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    "source": "PubMed",
                    "year": year,
                    "pmid": pmid,
                    "doi": ""  # PubMed doesn't always provide DOI easily
                })

            except Exception as e:
                # Skip malformed articles
                continue

        return papers

    except Exception as e:
        print(f"PubMed fetch error: {e}")
        return []


def fetch_pmc_papers(query: str, limit: int = 4) -> List[Dict[str, Any]]:
    """
    Fetch papers from PubMed Central (open access full-text articles).

    Args:
        query: Search query string
        limit: Maximum number of papers to fetch

    Returns:
        List of paper dicts with title, abstract, url, source, year, pmid
    """
    papers = []

    try:
        # Search PMC database
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        search_params = {
            "db": "pmc",
            "term": query,
            "retmax": limit,
            "retmode": "json"
        }

        search_response = requests.get(search_url, params=search_params, timeout=8)

        if search_response.status_code != 200:
            return []

        search_data = search_response.json()
        pmc_ids = search_data.get('esearchresult', {}).get('idlist', [])

        if not pmc_ids:
            return []

        # Fetch details
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        fetch_params = {
            "db": "pmc",
            "id": ",".join(pmc_ids),
            "retmode": "json"
        }

        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=8)

        if fetch_response.status_code != 200:
            return []

        summaries = fetch_response.json()

        for pmc_id in pmc_ids:
            try:
                article = summaries.get('result', {}).get(pmc_id, {})

                if not article:
                    continue

                title = article.get('title', 'No title')

                # PMC summaries don't include abstracts, use title as abstract fallback
                abstract = f"Open access article: {title[:200]}"

                # Extract year from pubdate
                pubdate = article.get('pubdate', 'N/A')
                year = pubdate.split()[0] if pubdate != 'N/A' else 'N/A'

                papers.append({
                    "title": title,
                    "abstract": abstract,
                    "url": f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/",
                    "source": "PMC",
                    "year": year,
                    "pmid": "",  # PMC uses different ID
                    "doi": article.get('doi', '')
                })

            except Exception as e:
                continue

        return papers

    except Exception as e:
        print(f"PMC fetch error: {e}")
        return []


def fetch_europe_pmc_papers(query: str, limit: int = 4) -> List[Dict[str, Any]]:
    """Fetch papers from Europe PMC."""
    pass  # Will implement later


def deduplicate_papers(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate papers by PMID, DOI, or title similarity."""
    pass  # Will implement later


def fetch_all_papers_parallel(query: str) -> List[Dict[str, Any]]:
    """Fetch papers from all sources in parallel."""
    pass  # Will implement later
