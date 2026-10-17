import sys
import requests
import xml.etree.ElementTree as ET

# Set stdout to UTF-8 to handle any special characters on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class PubMedFetcher:
    """
    Queries the NCBI Entrez API to retrieve research article titles, journals, 
    links, and abstracts on demand.
    """
    def __init__(self):
        self.base_search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.base_fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def fetch_abstracts(self, query: str, max_results: int = 3):
        """
        Searches PubMed and returns a list of dictionaries with study details.
        """
        # Step 1: Search for IDs matching the query
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": max_results
        }
        
        try:
            r = requests.get(self.base_search_url, params=search_params, timeout=10)
            r.raise_for_status()
            search_data = r.json()
            id_list = search_data.get("esearchresult", {}).get("idlist", [])
            
            if not id_list:
                return []
                
            # Step 2: Fetch details (including abstracts) for the returned IDs
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "retmode": "xml"
            }
            
            r_fetch = requests.get(self.base_fetch_url, params=fetch_params, timeout=15)
            r_fetch.raise_for_status()
            
            return self._parse_pubmed_xml(r_fetch.text)
            
        except Exception as e:
            print(f"Error fetching from PubMed: {e}")
            return []

    def _parse_pubmed_xml(self, xml_text: str):
        """
        Parses XML output from efetch.fcgi to extract title, abstract, authors, and metadata.
        """
        articles = []
        try:
            root = ET.fromstring(xml_text)
            for article in root.findall(".//PubmedArticle"):
                # Title
                title_node = article.find(".//ArticleTitle")
                title = "".join(title_node.itertext()).strip() if title_node is not None else "No Title Available"
                
                # Abstract
                abstract_nodes = article.findall(".//AbstractText")
                abstract_list = []
                for node in abstract_nodes:
                    label = node.get("Label")
                    text = "".join(node.itertext()).strip()
                    if label:
                        abstract_list.append(f"**{label}**: {text}")
                    else:
                        abstract_list.append(text)
                abstract = "\n\n".join(abstract_list) if abstract_list else "No Abstract Available"
                
                # Journal
                journal_node = article.find(".//Journal/Title")
                journal = journal_node.text if journal_node is not None else "Unknown Journal"
                
                # PubDate Year
                year_node = article.find(".//JournalIssue/PubDate/Year")
                year = year_node.text if year_node is not None else "N/A"
                if year == "N/A":
                    # Fallback to MedlineDate if Year is not explicitly parsed
                    medline_date = article.find(".//JournalIssue/PubDate/MedlineDate")
                    if medline_date is not None:
                        year = medline_date.text.split()[0]
                
                # PMCID / DOI / PMID
                pmid_node = article.find(".//PMID")
                pmid = pmid_node.text if pmid_node is not None else ""
                
                elocation_node = article.find(".//ELocationID[@EIdType='doi']")
                doi = elocation_node.text if elocation_node is not None else ""
                
                articles.append({
                    "title": title,
                    "abstract": abstract,
                    "journal": journal,
                    "year": year,
                    "pmid": pmid,
                    "doi": doi,
                    "link": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else f"https://doi.org/{doi}" if doi else ""
                })
        except Exception as e:
            print(f"Error parsing XML: {e}")
        return articles

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python PubMed_fetcher.py <query>")
        sys.exit(1)
        
    query_term = " ".join(sys.argv[1:])
    fetcher = PubMedFetcher()
    results = fetcher.fetch_abstracts(query_term, max_results=2)
    
    print(f"\nFetched {len(results)} results for query: '{query_term}':\n")
    for idx, paper in enumerate(results, 1):
        print(f"[{idx}] {paper['title']}")
        print(f"    Journal: {paper['journal']} ({paper['year']})")
        print(f"    Link: {paper['link']}")
        print(f"    Abstract snippet: {paper['abstract'][:300]}...\n")
