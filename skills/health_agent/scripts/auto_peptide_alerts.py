import os
import sys
import json
import requests

# Set stdout to UTF-8 to handle any special characters on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Resolve paths to import HermesBot and router
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "Project Hermes"))

try:
    from hermes_bot import HermesBot
except ImportError:
    # Fallback dummy class if running standalone or Project Hermes path issues
    class HermesBot:
        def send_alert(self, category, message):
            print(f"\n[HERMES ALERT] [{category}] {message}\n")

CACHE_FILE = os.path.join(script_dir, "seen_articles.json")

# Peptides / supplements to monitor
COMPOUNDS = ["BPC-157", "Urolithin A", "Fisetin", "Collagen Peptides"]

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_cache(seen_set):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(list(seen_set), f, indent=2)
    except Exception as e:
        print(f"Error saving cache: {e}")

def check_new_publications():
    seen_articles = load_cache()
    hermes = HermesBot()
    new_seen = set(seen_articles)
    
    print("Checking for new peptide & supplement research publications...")
    
    for compound in COMPOUNDS:
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        # Search for publications matching the compound name
        params = {
            "query": f"{compound} AND (peptide OR supplementation OR therapy OR longevity)",
            "format": "json",
            "resultType": "lite",
            "pageSize": 5
        }
        
        try:
            r = requests.get(url, params=params, timeout=10)
            if r.status_code != 200:
                continue
                
            data = r.json()
            results = data.get("resultList", {}).get("result", [])
            
            for paper in results:
                paper_id = paper.get("id")
                if not paper_id:
                    continue
                    
                # If article is new (not in seen cache)
                if paper_id not in seen_articles:
                    title = paper.get("title", "No Title Available")
                    journal = paper.get("journalTitle", "Unknown Journal")
                    year = paper.get("pubYear", "N/A")
                    doi = paper.get("doi", "")
                    link = f"https://doi.org/{doi}" if doi else f"PubMed ID: {paper_id}"
                    
                    alert_message = f"New study published on {compound} in {journal} ({year}): '{title}'. Read here: {link}"
                    
                    # Fire alert through Project Hermes
                    hermes.send_alert("RESEARCH", alert_message)
                    
                    new_seen.add(paper_id)
                    
        except Exception as e:
            print(f"Error checking research for {compound}: {e}")
            
    save_cache(new_seen)

if __name__ == "__main__":
    check_new_publications()
