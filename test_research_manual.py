from research_fetcher import fetch_pubmed_papers, fetch_pmc_papers, fetch_europe_pmc_papers

# Test Europe PMC
print("\n" + "="*60)
print("Testing Europe PMC")
print("="*60)
eu_papers = fetch_europe_pmc_papers("heart disease prevention", limit=3)
print(f"Found {len(eu_papers)} papers")
for i, paper in enumerate(eu_papers, 1):
    print(f"\n[{i}] {paper['title']}")
    print(f"    Year: {paper['year']}, Source: {paper['source']}")
    print(f"    Abstract: {paper['abstract'][:100]}...")
    print(f"    URL: {paper['url']}")
