# Research-Heavy Citation System Design

**Date:** 2026-04-21  
**Status:** Approved  
**Goal:** Make AI analysis cite 8-10 research papers inline with `[1][2]` format, backed by actual abstracts for authenticity.

---

## Problem Statement

**Current Issues:**
1. Citations displayed at bottom but NOT referenced inline in AI analysis
2. Only fetches from 2 sources (PubMed + Semantic Scholar)
3. Semantic Scholar is rate-limited (429 errors)
4. AI receives only paper titles, not abstracts (shallow understanding)
5. Search uses only first 500 chars of transcript (misses key medical terms)
6. Analysis feels generic, not research-backed

**User Need:**
Analysis should feel authentic and research-backed with inline citations like academic papers: "Studies show X [1][2]. However, recent findings suggest Y [3][4]."

**Target:** 8-10 papers per analysis with abstracts

---

## Design Goals

1. **Authentic citations** - AI cites papers inline using `[1][2]` format
2. **Research-backed** - AI reads abstracts to understand what papers actually say
3. **Credible sources** - Fetch from 3 medical databases: PubMed, PMC, Europe PMC
4. **Fast** - Parallel API calls keep total time under 15 seconds
5. **Reliable** - Graceful degradation if APIs fail
6. **Free** - All APIs used are free with generous limits
7. **Simple** - No RAG, no vector DBs, no complex dependencies

---

## Architecture Overview

### High-Level Flow

```
Full Transcript
    ↓
Extract Medical Keywords (regex pattern matching)
    ↓
Parallel Fetch (ThreadPool):
  ├─ PubMed API (3-4 papers + abstracts)
  ├─ PMC API (3-4 papers + abstracts)
  └─ Europe PMC API (3-4 papers + abstracts)
    ↓
Deduplicate by PMID/DOI (keep 8-10 unique papers)
    ↓
Single LLM Call:
  - Input: Transcript + Papers with Abstracts
  - Instruction: "Cite papers using [1][2] format"
  - Output: Analysis with inline citations
    ↓
Display:
  - Analysis text with clickable [1][2] links
  - Citations section with paper details
```

### Why This Architecture?

**Parallel over Sequential:**
- 3 APIs called simultaneously = faster (10-15 sec vs 30+ sec)
- Modern, professional approach

**Abstracts over Full Text:**
- Enough context for AI understanding
- Token-efficient (~4000 tokens total)
- Free APIs provide abstracts readily

**Single LLM Call (No Claim Extraction):**
- Simpler than RAG pipeline
- Faster (no extra LLM call for claim extraction)
- Works well for 1-3 claim reels (most common)

**Three Medical Sources:**
- PubMed: Most authoritative, NCBI-backed
- PMC: Full-text open access papers
- Europe PMC: European medical research, good coverage
- Removes unreliable Semantic Scholar

---

## Component Design

### Component 1: Keyword Extractor

**Location:** `app.py` (new function)

**Function Signature:**
```python
def extract_medical_keywords(transcript: str) -> str
```

**Purpose:** Extract medical terms from full transcript for targeted paper searches

**Implementation Strategy (Regex-based, no NLP libraries needed):**
1. Use regex patterns to find:
   - Drug/supplement names (capitalized multi-word terms)
   - Medical conditions (words ending in "itis", "osis", "emia")
   - Vitamins/minerals (vitamin D, calcium, etc.)
   - Body parts/systems (heart, liver, immune, etc.)
   - Treatment terms (therapy, treatment, cure, etc.)

2. Remove stop words (the, and, or, but, etc.)

3. Return top 10-15 keywords as space-separated string

4. Fallback: If no keywords found, use first 200 chars of transcript

5. Max length: 150 characters (API query limits)

**Example:**
- Input: "Turmeric helps with inflammation and joint pain in arthritis patients drinking warm water"
- Output: "turmeric inflammation joint pain arthritis"

**Edge Cases:**
- Empty transcript → Return "medical health"
- Hindi/mixed language → Use language-agnostic patterns (medical terms often English)
- Very short transcript (<50 chars) → Use full transcript

---

### Component 2: Research Fetcher (Parallel API Handler)

**Location:** `research_fetcher.py` (NEW FILE)

**Main Function:**
```python
def fetch_all_papers_parallel(query: str) -> List[Dict[str, str]]
```

**Returns:** List of papers with structure:
```python
{
    "title": str,
    "abstract": str,      # NEW - full abstract text
    "url": str,           # Direct link to paper
    "source": str,        # "PubMed", "PMC", "Europe PMC"
    "year": str,          # Publication year
    "pmid": str,          # PubMed ID (for deduplication)
    "doi": str,           # DOI (for deduplication)
}
```

**Implementation:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

def fetch_all_papers_parallel(query: str) -> List[Dict]:
    """Fetch papers from 3 sources simultaneously"""
    
    papers = []
    
    # Define API fetch functions
    apis = [
        (fetch_pubmed_papers, query, 4),
        (fetch_pmc_papers, query, 4),
        (fetch_europe_pmc_papers, query, 4),
    ]
    
    # Execute in parallel with timeout
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(func, q, limit): source 
            for func, q, limit in apis
        }
        
        for future in as_completed(futures, timeout=10):
            try:
                result = future.result(timeout=8)
                papers.extend(result)
            except Exception as e:
                # Log error, continue with other sources
                print(f"API failed: {e}")
                continue
    
    # Deduplicate and limit to 10
    papers = deduplicate_papers(papers)
    return papers[:10]
```

---

#### Sub-component: PubMed Fetcher

**Function:**
```python
def fetch_pubmed_papers(query: str, limit: int = 4) -> List[Dict]
```

**API Endpoints:**
1. Search: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
2. Fetch: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`

**Implementation Steps:**
1. Search for PMIDs matching query
2. Fetch paper details including abstract using `efetch` with `retmode=xml`
3. Parse XML to extract: title, abstract, year, PMID
4. Build paper dict with URL: `https://pubmed.ncbi.nlm.nih.gov/{pmid}/`

**Rate Limits:** 3 req/sec (we do 1-2, safe)

**Error Handling:**
- Timeout after 8 seconds
- Return empty list on failure
- Log errors in debug mode

---

#### Sub-component: PMC Fetcher

**Function:**
```python
def fetch_pmc_papers(query: str, limit: int = 4) -> List[Dict]
```

**API Endpoint:**
`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc`

**Implementation:**
- Similar to PubMed but use `db=pmc` parameter
- PMC IDs start with "PMC" prefix
- URL format: `https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/`
- Abstracts available in most open-access papers

**Difference from PubMed:**
- PMC = Full-text open access articles
- PubMed = Abstracts + citations
- PMC subset of PubMed, but different indexing

---

#### Sub-component: Europe PMC Fetcher

**Function:**
```python
def fetch_europe_pmc_papers(query: str, limit: int = 4) -> List[Dict]
```

**API Endpoint:**
`https://www.ebi.ac.uk/europepmc/webservices/rest/search`

**Parameters:**
```python
params = {
    "query": query,
    "format": "json",
    "pageSize": limit,
    "resultType": "core"
}
```

**Implementation:**
- Returns JSON with title, abstract, DOI, year
- URL: Use DOI link `https://doi.org/{doi}`
- Source tag: "Europe PMC"

**Rate Limits:** 10 req/sec (very generous)

---

#### Sub-component: Deduplicator

**Function:**
```python
def deduplicate_papers(papers: List[Dict]) -> List[Dict]
```

**Deduplication Strategy:**
1. Check PMID (if exists) - exact match
2. Check DOI (if exists) - exact match
3. Fuzzy title match - >90% similarity (using `difflib.SequenceMatcher`)
4. Keep first occurrence (PubMed preferred)

**Example:**
```python
from difflib import SequenceMatcher

def are_duplicates(paper1, paper2):
    # Check PMID
    if paper1.get('pmid') and paper1['pmid'] == paper2.get('pmid'):
        return True
    
    # Check DOI
    if paper1.get('doi') and paper1['doi'] == paper2.get('doi'):
        return True
    
    # Fuzzy title match
    ratio = SequenceMatcher(None, 
                           paper1['title'].lower(), 
                           paper2['title'].lower()).ratio()
    return ratio > 0.9
```

**Output:** Unique list of 8-10 papers max

---

### Component 3: LLM Prompt Engineering

**Location:** `app.py` → `analyze_with_llm()` (MODIFIED)

**Changes:**
1. Accept `papers_with_abstracts` parameter
2. Build numbered reference list for prompt
3. Add explicit instruction to cite inline
4. Return analysis + citation mapping

**New Function Signature:**
```python
def analyze_with_llm(
    caption: str, 
    transcript: str, 
    papers: List[Dict]
) -> Tuple[str, List[Dict]]
```

**Prompt Structure:**
```python
# Build numbered paper list
papers_text = ""
for i, paper in enumerate(papers, 1):
    papers_text += f"""
[{i}] Title: "{paper['title']}" ({paper['year']})
    Source: {paper['source']}
    Abstract: {paper['abstract'][:250]}...
    
"""

prompt = f"""You are a Gen-Z medical fact-checker. Analyze this Instagram Reel 
and CITE the research papers inline using [1], [2], [3] format.

**Caption:** {caption}

**Transcript:** {transcript}

**Research Papers Available (CITE THESE):**
{papers_text}

Your task:
1. **What's the claim?** - Summarize (max 2 lines)
2. **Is it legit?** ✅❌ - Rate accuracy with CITATIONS
3. **The tea ☕** - Explain truth with citations [1][2]
4. **Red flags 🚩** - Point out errors with citations [3][4]
5. **Bottom line** - Verdict

IMPORTANT:
- Use inline citations like: "Studies show X [1][2]. However, Y [3]."
- Cite papers that support or refute specific claims
- Be accurate, funny, Gen-Z friendly

Example: "Turmeric contains curcumin which reduces inflammation [1][2], 
but needs piperine for absorption [3]."
"""
```

**LLM Call:**
```python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a medical fact-checker who cites research inline using [1][2] format."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=2048
)

analysis = response.choices[0].message.content
```

**Return:**
- Formatted analysis text (with HTML)
- Original papers list (for display_citations)

---

### Component 4: Citation Display

**Location:** `app.py` → `display_citations()` (ENHANCED)

**Changes:**
1. Add citation number badges `[1]`, `[2]`
2. Keep existing beautiful CSS styling
3. Make inline `[1]` in analysis text clickable (hyperlink to citation section)
4. Show abstract excerpt (first 150 chars + "...")

**Enhanced Display:**
```markdown
📚 Scientific References (10 sources)

💡 Transparency Note: Click links to verify sources used in this analysis.

[1] 🔬 Turmeric and Inflammatory Response in Clinical Trials (2023)
    PubMed • PMID: 12345678
    "Clinical trial of 200 patients with rheumatoid arthritis found that 
    curcumin supplementation reduced inflammatory markers..."
    🔗 View Full Paper

[2] 📄 Curcumin Absorption and Bioavailability Meta-Analysis (2024)
    Europe PMC • DOI: 10.1234/example
    "Systematic review of 50 studies concluded that curcumin absorption 
    is significantly enhanced when combined with piperine..."
    🔗 View Full Paper
```

**Implementation:**
- Parse analysis text for `[1]`, `[2]` patterns
- Replace with clickable anchor links: `<a href="#citation-1">[1]</a>`
- Add `id="citation-1"` to citation display elements
- Truncate abstracts to 150 chars for readability

---

## Data Flow (Detailed)

### Step 1: User Input
```
User pastes Instagram reel URL
  ↓
Click "Analyze This Reel!"
```

### Step 2: Reel Processing (Existing)
```
Fetch reel data from RapidAPI
  ↓
Extract caption
  ↓
Download audio
  ↓
Transcribe audio (Hindi/English)
  ↓
Full transcript text
```

### Step 3: Research Pipeline (NEW)
```
extract_medical_keywords(transcript)
  ↓
Keywords: "turmeric inflammation arthritis"
  ↓
fetch_all_papers_parallel(keywords)
  ├─ Thread 1: PubMed → 4 papers
  ├─ Thread 2: PMC → 3 papers (1 failed)
  └─ Thread 3: Europe PMC → 4 papers
  ↓
11 papers collected
  ↓
deduplicate_papers() → 9 unique papers (keep best 8-10)
  ↓
Papers with abstracts ready
```

### Step 4: LLM Analysis (MODIFIED)
```
analyze_with_llm(caption, transcript, papers)
  ↓
Build prompt with numbered papers [1]-[9]
  ↓
Groq LLM call (5000 tokens)
  ↓
Analysis text with [1][2][3] citations
  ↓
format_analysis_with_proper_markdown()
  ↓
Replace [1] with <a href="#citation-1">[1]</a>
```

### Step 5: Display (ENHANCED)
```
Show analysis with clickable citations
  ↓
<hr>
  ↓
display_citations(papers) - numbered list
  ↓
Chat interface (citations in context)
```

---

## Error Handling & Edge Cases

### Scenario 1: All APIs Fail
**Trigger:** Network down, all 3 APIs timeout/error

**Handling:**
```python
if len(papers) == 0:
    st.warning("⚠️ Research databases unavailable. Analysis based on general medical knowledge.")
    # Continue with LLM analysis, no citations
    return analyze_with_llm(caption, transcript, papers=[])
```

**User Experience:**
- Still get analysis (using LLM's built-in knowledge)
- Clear warning about missing citations
- No app crash

---

### Scenario 2: Partial API Failures
**Trigger:** 1-2 APIs work, others fail

**Handling:**
```python
if 1 <= len(papers) < 5:
    st.info(f"ℹ️ Found {len(papers)} references. Some databases unavailable.")
elif len(papers) >= 5:
    st.success(f"✅ Found {len(papers)} scientific references!")
```

**User Experience:**
- Analysis proceeds with available papers (better than nothing)
- Transparent about partial success

---

### Scenario 3: No Medical Keywords Found
**Trigger:** Non-medical reel (fitness, lifestyle)

**Handling:**
```python
keywords = extract_medical_keywords(transcript)
if not keywords or len(keywords) < 10:
    # Fallback to first 200 chars
    keywords = transcript[:200]
```

**User Experience:**
- Broad search still finds relevant papers
- Works for edge cases

---

### Scenario 4: Abstracts Missing
**Trigger:** Some papers don't have abstracts

**Handling:**
```python
abstract = paper.get('abstract', 'Abstract not available')
if abstract == 'Abstract not available':
    # Use title + metadata only
    abstract = f"Study on {paper['title']}"
```

**User Experience:**
- LLM still cites paper by title
- Less context, but citation still valid

---

### Scenario 5: LLM Doesn't Cite Inline
**Trigger:** LLM ignores instruction, writes without [1][2]

**Detection:**
```python
import re
citation_pattern = r'\[\d+\]'
citations_found = re.findall(citation_pattern, analysis)

if len(citations_found) == 0 and len(papers) > 0:
    st.warning("ℹ️ Note: Analysis may not explicitly reference all papers listed below.")
```

**User Experience:**
- Show warning
- Still display citations at bottom
- User knows to read both sections

---

### Scenario 6: API Rate Limiting
**Trigger:** Too many requests, API returns 429

**Handling:**
```python
def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait_time)
        except Timeout:
            continue
    return None  # Give up after retries
```

**User Experience:**
- Automatic retry with backoff
- If all retries fail, skip that API gracefully

---

## Token Management

### Current Token Usage
- Transcript: ~500 tokens
- Prompt: ~500 tokens
- LLM response: ~500 tokens
- **Total: ~1500 tokens/analysis**

### New Token Usage (After Optimization)
- Transcript: ~500 tokens
- Papers (10 papers × 250 words truncated): ~3500 tokens
- System prompt: ~400 tokens
- LLM response: ~500 tokens
- **Total: ~4900 tokens/analysis**

### Optimization Strategy
1. Truncate abstracts to 250 words max (from 300-400 typical)
2. Remove redundant prompt text
3. Limit to 10 papers max (not 12+)
4. **Final target: ~4900 tokens/analysis**

### Groq API Limits
- Free tier: 30 req/min, 15k tokens/min
- Our usage: 4500 tokens = **3 analyses/minute**
- **Status: Within limits ✅**

---

## File Structure Changes

### New Files
```
Instagram_reel_buster/
├── research_fetcher.py          # NEW - Parallel API fetcher
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-04-21-research-citations-design.md  # This file
```

### Modified Files
```
Instagram_reel_buster/
├── app.py                       # MODIFIED - Add keyword extraction, modify LLM call
└── requirements.txt             # No changes (concurrent.futures is built-in)
```

---

## Implementation Checklist

### Phase 1: Research Fetcher (New File)
- [ ] Create `research_fetcher.py`
- [ ] Implement `fetch_pubmed_papers()`
- [ ] Implement `fetch_pmc_papers()`
- [ ] Implement `fetch_europe_pmc_papers()`
- [ ] Implement `fetch_all_papers_parallel()`
- [ ] Implement `deduplicate_papers()`
- [ ] Add error handling and timeouts
- [ ] Test each API individually
- [ ] Test parallel execution

### Phase 2: Keyword Extraction (app.py)
- [ ] Add `extract_medical_keywords()` function
- [ ] Implement regex patterns for medical terms
- [ ] Add fallback logic
- [ ] Test with various transcripts (Hindi, English, mixed)

### Phase 3: LLM Integration (app.py)
- [ ] Modify `analyze_with_llm()` to accept papers parameter
- [ ] Build numbered paper list in prompt
- [ ] Add inline citation instruction
- [ ] Test LLM response with sample papers
- [ ] Verify [1][2] citations appear in output

### Phase 4: Citation Display (app.py)
- [ ] Enhance `display_citations()` with numbering
- [ ] Add abstract excerpts
- [ ] Make inline [1][2] clickable (anchor links)
- [ ] Test responsive styling
- [ ] Verify dark mode compatibility

### Phase 5: Integration Testing
- [ ] End-to-end test with real reel URL
- [ ] Verify research pipeline works
- [ ] Check citation links
- [ ] Test error scenarios (API failures)
- [ ] Performance test (measure total time)

### Phase 6: Polish
- [ ] Add loading indicators for research fetch
- [ ] Improve error messages
- [ ] Update debug mode to show research pipeline details
- [ ] Test with 10+ different medical reels

---

## Testing Strategy

### Unit Tests (Manual Verification)
1. **Keyword Extraction**
   - Test: Medical transcript → Extract keywords
   - Test: Non-medical transcript → Fallback to first 200 chars
   - Test: Empty transcript → Handle gracefully

2. **Individual APIs**
   - Test: PubMed with query "diabetes" → Get 4 papers with abstracts
   - Test: PMC with query "cancer" → Get papers
   - Test: Europe PMC with query "heart disease" → Get papers
   - Verify: All return correct structure

3. **Parallel Fetching**
   - Test: Query all 3 APIs → All complete within 10 seconds
   - Test: Kill one API → Others continue
   - Test: All APIs timeout → Graceful failure

4. **Deduplication**
   - Test: Feed 2 identical papers (same PMID) → Keep 1
   - Test: Feed papers with similar titles → Detect duplicates
   - Test: Feed 15 unique papers → Return 10 max

5. **LLM Citation**
   - Test: Provide 5 papers → Verify [1][2][3] appear in response
   - Test: Provide 0 papers → Analysis without citations
   - Verify: Citations are relevant to claims

### Integration Tests
1. **End-to-End**
   - Input: Real Instagram reel URL
   - Expected: Analysis with 5-10 inline citations
   - Verify: Citations clickable, papers display correctly

2. **Error Scenarios**
   - Test: Network disconnected → Show warning, continue
   - Test: Invalid reel URL → Handle gracefully
   - Test: Non-medical reel → Still get some papers

3. **Rate Limiting**
   - Test: 5 rapid analyses → No rate limit errors
   - Monitor: API response times

4. **Edge Cases**
   - Test: Very short transcript (10 words) → Handle
   - Test: Very long transcript (1000+ words) → Truncate appropriately
   - Test: Hindi-only transcript → Extract keywords or fallback

### User Acceptance Testing
- Test with 10 real medical reels
- Verify citations feel authentic and relevant
- Check analysis quality with citations vs without
- Measure average time (target: <20 seconds)

---

## Success Metrics

### Functional Requirements
- ✅ Analysis includes inline citations [1][2] format
- ✅ 8-10 papers displayed with abstracts
- ✅ Citations clickable and link to papers
- ✅ Works with 3 medical APIs (PubMed, PMC, Europe PMC)
- ✅ Graceful degradation if APIs fail

### Performance Requirements
- ✅ Total analysis time < 20 seconds
- ✅ Research fetch < 10 seconds (parallel)
- ✅ Within Groq token limits (4500 tokens)

### Quality Requirements
- ✅ Citations are relevant to claims in reel
- ✅ Papers from credible medical sources
- ✅ Analysis references papers appropriately
- ✅ UI responsive on mobile

---

## Future Enhancements (Out of Scope)

These are explicitly NOT part of this design but could be future work:

1. **Claim-by-claim search** - Extract multiple claims, search separately
2. **RAG pipeline** - Vector DB + embeddings for better paper matching
3. **Full-text analysis** - Fetch full papers (requires paid APIs)
4. **Citation quality scoring** - Rank papers by relevance/impact factor
5. **Multi-language support** - Translate keywords for non-English APIs
6. **Caching** - Cache paper results for common topics
7. **User feedback** - "Was this citation helpful?" ratings

---

## Dependencies & Requirements

### Python Packages (No New Dependencies)
- `concurrent.futures` - Built-in Python 3.2+
- `requests` - Already in requirements.txt
- `streamlit` - Already in requirements.txt
- `groq` - Already in requirements.txt
- `difflib` - Built-in Python standard library

### External APIs (All Free)
- PubMed E-utilities - NCBI
- PubMed Central (PMC) - NCBI
- Europe PMC - EMBL-EBI

### Environment Variables (.env)
No new variables needed. Existing:
```
GROQ_API_KEY_1=...
GROQ_API_KEY_2=...
GROQ_API_KEY_3=...
RAPIDAPI_KEY=...
```

---

## Deployment Considerations

### Streamlit Cloud
- No new packages to add to `packages.txt`
- All APIs are public, no firewall issues
- Token usage within free tier

### Local Development
- Works immediately (no new installs)
- Fast on modern hardware (parallel = efficient)

### Production Concerns
- API rate limits: 3 req/min per user = safe for 100s of users
- If scaling: Add caching layer (Redis) for popular topics
- Monitor: API success rates, average fetch times

---

## Risk Assessment

### Low Risk
- PubMed/PMC APIs stable and well-documented
- No new dependencies to install
- Backward compatible (fallback to old behavior if research fails)

### Medium Risk
- Europe PMC less known (but documented and stable)
- LLM might not always cite inline (detection + warning handles this)

### High Risk
- None identified

### Mitigation Strategies
- Comprehensive error handling at every API call
- Fallback to general knowledge if all research fails
- Debug mode to troubleshoot issues
- Graceful degradation preserves core functionality

---

## Rollback Plan

If implementation fails or causes issues:

1. **Research fetcher isolated** - Can disable by returning empty list
2. **LLM analysis still works** - Falls back to no-citation mode
3. **No breaking changes** - Existing functionality preserved
4. **Easy rollback** - Delete `research_fetcher.py`, revert `app.py` changes

**Rollback trigger:** If >50% of analyses fail to get citations after 1 week

---

## Conclusion

This design provides a **fast, simple, and authentic** research citation system that:

- Fetches 8-10 papers from 3 credible medical sources
- Provides abstracts to LLM for real understanding
- Generates inline citations [1][2] in Gen-Z friendly analysis
- Handles errors gracefully
- Stays within free API limits
- Requires no new dependencies
- Takes <20 seconds end-to-end

The parallel architecture keeps it fast while multiple sources ensure reliability. The hybrid approach (abstracts without RAG) balances authenticity with simplicity.

**Next Step:** Create implementation plan with step-by-step tasks.
