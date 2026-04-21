from research_fetcher import fetch_pubmed_papers, fetch_pmc_papers

# Test PMC
print("\n" + "="*60)
print("Testing PMC")
print("="*60)
pmc_papers = fetch_pmc_papers("cancer immunotherapy", limit=3)
print(f"Found {len(pmc_papers)} papers")
for i, paper in enumerate(pmc_papers, 1):
    print(f"\n[{i}] {paper['title']}")
    print(f"    Year: {paper['year']}, Source: {paper['source']}")
    print(f"    URL: {paper['url']}")
