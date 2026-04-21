from research_fetcher import fetch_all_papers_parallel

print("="*60)
print("Testing Parallel Fetch with Deduplication")
print("="*60)

query = "turmeric inflammation arthritis"
print(f"\nQuery: {query}")
print("Fetching from PubMed, PMC, and Europe PMC in parallel...\n")

papers = fetch_all_papers_parallel(query)

print(f"\n{'='*60}")
print(f"Total unique papers: {len(papers)}")
print(f"{'='*60}\n")

for i, paper in enumerate(papers, 1):
    print(f"[{i}] {paper['title']}")
    print(f"    Source: {paper['source']} | Year: {paper['year']}")
    print(f"    Abstract: {paper['abstract'][:150]}...")
    print(f"    URL: {paper['url']}")
    print()
