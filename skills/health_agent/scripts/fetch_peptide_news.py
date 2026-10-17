import sys
import requests

# Set stdout to UTF-8 to handle any special characters in titles/authors on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def search_europe_pmc(query):
    print(f"Searching Europe PMC for: '{query}'...")
    
    # We restrict search query to scientific papers on peptides, adding terms if needed
    search_query = f"{query} AND (peptide OR supplementation OR therapy)"
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": search_query,
        "format": "json",
        "resultType": "lite",
        "pageSize": 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            return
            
        data = response.json()
        results = data.get("resultList", {}).get("result", [])
        
        if not results:
            print("\nNo recent publications found matching this peptide query.")
            return
            
        print(f"\n=== LATEST PEPTIDE RESEARCH & NEWS FOR: {query.upper()} ===")
        for idx, paper in enumerate(results, 1):
            title = paper.get("title", "No Title Available")
            authors = paper.get("authorString", "Unknown Authors")
            journal = paper.get("journalTitle", "Unknown Journal")
            year = paper.get("pubYear", "N/A")
            pmid = paper.get("id", "")
            doi = paper.get("doi", "")
            
            # Avoid potential print encoding crashes on console
            try:
                print(f"\n[{idx}] {title}")
                print(f"    Journal: {journal} ({year})")
                print(f"    Authors: {authors[:120]}..." if len(authors) > 120 else f"    Authors: {authors}")
                if doi:
                    print(f"    Link: https://doi.org/{doi}")
                elif pmid:
                    print(f"    PubMed ID: {pmid}")
            except UnicodeEncodeError:
                # Fallback if encoding still fails
                print(f"\n[{idx}] [Title contains special characters]")
                print(f"    Journal: {journal} ({year})")
                if doi:
                    print(f"    Link: https://doi.org/{doi}")
        print("\n========================================================")
        
    except requests.exceptions.Timeout:
        print("Error: The request to Europe PMC timed out.")
    except Exception as e:
        print(f"Error occurred while fetching publications: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_peptide_news.py <peptide_name>")
        sys.exit(1)
        
    query_peptide = " ".join(sys.argv[1:])
    search_europe_pmc(query_peptide)
