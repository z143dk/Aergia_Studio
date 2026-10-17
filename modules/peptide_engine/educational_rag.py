import os
import sys
import json

# Set stdout to UTF-8 to handle any special characters on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Resolve paths to import the intelligence router
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(script_dir))
sys.path.append(root_dir)

try:
    from intelligence_router import router, TaskType
except ImportError:
    # Dummy mock fallback
    class MockRouter:
        def generate(self, prompt, task_type=None, system_prompt=""):
            print("WARNING: Using Mock Router. Output is static.")
            return "Local inference not available. Setup API keys or start Ollama."
    router = MockRouter()
    TaskType = None

from modules.peptide_engine.PubMed_fetcher import PubMedFetcher

class PeptideEduEngine:
    def __init__(self):
        self.db_path = os.path.join(script_dir, "compound_database.json")
        self.fetcher = PubMedFetcher()
        self.database = self._load_database()

    def _load_database(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def extract_compound(self, query: str):
        """
        Attempts to identify if any compounds in our database are mentioned in the query.
        """
        query_lower = query.lower()
        for compound in self.database.keys():
            if compound.lower() in query_lower:
                return compound
        return None

    def query(self, user_query: str):
        compound = self.extract_compound(user_query)
        
        db_context = ""
        pubmed_context = ""
        search_term = user_query
        
        if compound:
            info = self.database[compound]
            search_term = " OR ".join(info.get("ncbi_mesh_terms", [compound]))
            db_context = (
                f"### DATABASE PROFILE FOR {compound.upper()}:\n"
                f"- **Class**: {info.get('class')}\n"
                f"- **Target Receptor**: {info.get('target_receptor')}\n"
                f"- **Primary Signaling Pathway**: {info.get('primary_pathway')}\n"
                f"- **Primary Physiological Effect**: {info.get('primary_effect')}\n"
                f"- **Half-Life**: {info.get('half_life')}\n"
            )
            print(f"Matched Database Compound: {compound}")
        else:
            print("No compound matched in local database. Performing open PubMed search...")

        # Fetch PubMed research abstracts
        print(f"Querying PubMed with search terms: '{search_term}'...")
        papers = self.fetcher.fetch_abstracts(search_term, max_results=3)
        
        if papers:
            pubmed_list = []
            for idx, paper in enumerate(papers, 1):
                pubmed_list.append(
                    f"Paper [{idx}]: {paper['title']}\n"
                    f"Journal: {paper['journal']} ({paper['year']})\n"
                    f"Abstract: {paper['abstract']}\n"
                    f"Source Link: {paper['link']}\n"
                )
            pubmed_context = "### NCBI PUBMED CLINICAL & PRECLINICAL EVIDENCE:\n" + "\n".join(pubmed_list)
        else:
            pubmed_context = "### NCBI PUBMED EVIDENCE:\nNo recent abstracts could be retrieved from PubMed."

        # Compile System Prompt directive
        system_prompt = (
            "System Directive for Aergia Peptide Edu Engine:\n"
            "You are an objective, medical-grade biochemistry learning assistant integrated into Hermes Mission Control. "
            "When queried about a peptide or metabolic compound:\n"
            "1. Explain the mechanism of action (MOA) at the cellular and receptor level.\n"
            "2. Outline the physiological signaling pathways involved (e.g., AMPK, cAMP, Sirtuins, BDNF).\n"
            "3. Distinguish between FDA-approved indications and preclinical/investigational research data.\n"
            "4. Reference clinical research methodologies without giving medical prescriptions or dosing advice.\n"
            "5. Strictly avoid anecdotal social media claims, hype, or unverified influencer protocols."
        )

        # Build prompt
        full_prompt = (
            f"User Query: {user_query}\n\n"
            f"{db_context}\n"
            f"{pubmed_context}\n\n"
            f"Based on the database profile and peer-reviewed PubMed abstracts above, synthesize a medical-grade explanation answering the user's query."
        )

        print("Generating synthesized biochemistry response...")
        
        # Route query through DeepSeek / Gemini or local Hermes 3
        try:
            # We use TaskType.REASONING for deep educational quality, fallback to speed
            task_type = TaskType.REASONING if TaskType else None
            response = router.generate(full_prompt, task_type=task_type, system_prompt=system_prompt)
            return response, papers
        except Exception as e:
            print(f"Error calling routing router: {e}")
            # Fallback to local speed model directly if router fails
            try:
                task_type = TaskType.SPEED if TaskType else None
                response = router.generate(full_prompt, task_type=task_type, system_prompt=system_prompt)
                return response, papers
            except Exception as ex:
                return f"Could not generate response. Error: {ex}", papers

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python educational_rag.py <question>")
        sys.exit(1)
        
    query_text = " ".join(sys.argv[1:])
    engine = PeptideEduEngine()
    response, papers = engine.query(query_text)
    
    print("\n=== 🎓 BIOCHEMISTRY REPORT ===")
    print(response)
    print("===============================")
