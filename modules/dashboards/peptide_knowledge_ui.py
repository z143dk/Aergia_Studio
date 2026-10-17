import os
import sys
import streamlit as st

# Set stdout to UTF-8 to handle any special characters on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Resolve paths to import the peptide engine
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(script_dir))
sys.path.append(root_dir)

from modules.peptide_engine.educational_rag import PeptideEduEngine

st.set_page_config(
    page_title="Aergia Peptide Biochemistry Engine",
    page_icon="🧬",
    layout="wide",
)

# Custom Premium Styling (Sleek Dark Mode & Glassmorphism)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    .stTextInput>div>div>input {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 8px;
    }
    
    .stSelectbox>div>div>div {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
    }
    
    /* Card design */
    .peptide-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }
    
    .peptide-title {
        color: #3b82f6;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .peptide-subtitle {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 400;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stat-label {
        font-weight: 600;
        color: #38bdf8;
    }
    
    .stat-val {
        color: #f8fafc;
        margin-bottom: 12px;
    }
    
    /* Article Card design */
    .paper-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .paper-title {
        color: #10b981;
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 4px;
    }
    
    .paper-meta {
        color: #94a3b8;
        font-size: 12px;
        margin-bottom: 8px;
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown("### 🏛️ PROJECT AERGIA // HERMES MISSION CONTROL")
st.title("🧬 Peptide Biochemistry & Educational Engine")
st.markdown(
    "Objective, medical-grade educational query engine powered by peer-reviewed PubMed research abstracts and local inference."
)
st.markdown("---")

# Initialize Engine
@st.cache_resource
def get_engine():
    return PeptideEduEngine()

engine = get_engine()

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📘 Compound Catalog")
    
    compounds = list(engine.database.keys())
    selected_comp = st.selectbox("Select a compound to analyze:", compounds)
    
    if selected_comp:
        info = engine.database[selected_comp]
        
        # Render a beautiful metadata card
        st.markdown(
            f"""
            <div class="peptide-card">
                <div class="peptide-title">{selected_comp}</div>
                <div class="peptide-subtitle">{info.get('class')}</div>
                
                <div class="stat-label">Target Receptor:</div>
                <div class="stat-val">{info.get('target_receptor')}</div>
                
                <div class="stat-label">Primary Signaling Pathway:</div>
                <div class="stat-val">{info.get('primary_pathway')}</div>
                
                <div class="stat-label">Primary Physiological Effect:</div>
                <div class="stat-val">{info.get('primary_effect')}</div>
                
                <div class="stat-label">Half-Life:</div>
                <div class="stat-val">{info.get('half_life')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Button to fetch quick PubMed abstracts
        if st.button(f"🔍 Fetch NCBI Abstracts for {selected_comp}"):
            with st.spinner("Accessing Entrez API..."):
                search_term = " OR ".join(info.get("ncbi_mesh_terms", [selected_comp]))
                papers = engine.fetcher.fetch_abstracts(search_term, max_results=3)
                
                if papers:
                    st.success(f"Retrieved {len(papers)} papers on {selected_comp}:")
                    for paper in papers:
                        st.markdown(
                            f"""
                            <div class="paper-card">
                                <div class="paper-title">{paper['title']}</div>
                                <div class="paper-meta">{paper['journal']} ({paper['year']}) &middot; <a href="{paper['link']}" target="_blank">PubMed Link</a></div>
                                <div><strong>Abstract:</strong> {paper['abstract'][:400]}...</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.warning("No recent papers found for this compound.")

with col2:
    st.header("🧠 Biochemistry Educational Query")
    
    user_query = st.text_input(
        "Ask a biochemically-focused question (e.g. 'How does MOTS-c activate skeletal muscle AMPK?'):",
        placeholder="Type your question here..."
    )
    
    if user_query:
        with st.spinner("Compiling database profiles, fetching PubMed literature, and generating RAG analysis..."):
            response, papers = engine.query(user_query)
            
            st.subheader("🤖 Synthesized Biochemistry Report")
            st.markdown(response)
            st.markdown("---")
            
            if papers:
                st.subheader("📚 Referenced Peer-Reviewed Literature")
                for paper in papers:
                    with st.expander(f"Paper: {paper['title']} ({paper['year']})"):
                        st.markdown(f"**Journal:** {paper['journal']}")
                        st.markdown(f"**Link:** [{paper['link']}]({paper['link']})")
                        st.markdown(f"**Abstract:**\n{paper['abstract']}")
            else:
                st.info("No external literature was matched for this specific query.")
