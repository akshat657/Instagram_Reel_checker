from research_fetcher import fetch_pubmed_papers

# Test PubMed
papers = fetch_pubmed_papers("diabetes treatment", limit=3)
print(f"Found {len(papers)} papers")
for i, paper in enumerate(papers, 1):
    print(f"\n[{i}] {paper['title']}")
    print(f"    Year: {paper['year']}, PMID: {paper['pmid']}")
    print(f"    Abstract: {paper['abstract'][:100]}...")
