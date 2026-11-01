"""
Financial RAG Assistant - SaaS-style Streamlit App
API key loaded from .env file only.
Run: streamlit run frontend/streamlit_app.py
"""

import os, re, io, sys, json
import streamlit as st
from dotenv import load_dotenv

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

load_dotenv(os.path.join(ROOT, ".env"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
KEY_OK = bool(GROQ_API_KEY) and "your_groq" not in GROQ_API_KEY

st.set_page_config(
    page_title="FinSight · Financial RAG Assistant",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# THEME / CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --brand: #6366f1;
  --brand-2: #8b5cf6;
  --brand-soft: rgba(99,102,241,.10);
  --border: rgba(128,128,150,.22);
  --card: rgba(128,128,150,.06);
  --ok: #10b981;
  --warn: #f59e0b;
  --err: #ef4444;
}

html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif !important; }

/* hide streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { padding-top: 1.4rem !important; padding-bottom: 5rem !important; max-width: 1180px; }

/* ── Sidebar ─────────────────────────────────────── */
section[data-testid="stSidebar"] { border-right: 1px solid var(--border); }
section[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }
.brand { display:flex; align-items:center; gap:12px; margin-bottom:4px; }
.brand-logo {
  width:40px; height:40px; border-radius:12px; display:grid; place-items:center;
  background: linear-gradient(135deg, var(--brand), var(--brand-2)); color:#fff; font-size:20px;
  box-shadow: 0 6px 18px rgba(99,102,241,.35);
}
.brand-name { font-weight:800; font-size:19px; letter-spacing:-.3px; line-height:1.1; }
.brand-sub  { font-size:12px; opacity:.6; }
.side-label {
  font-size:11px; font-weight:700; letter-spacing:.09em; text-transform:uppercase;
  opacity:.55; margin: 14px 0 6px;
}

/* status pill */
.pill {
  display:inline-flex; align-items:center; gap:7px; padding:5px 12px; border-radius:999px;
  font-size:12.5px; font-weight:600; border:1px solid var(--border); background: var(--card);
}
.dot { width:8px; height:8px; border-radius:50%; display:inline-block; }
.dot.ok  { background: var(--ok);  box-shadow: 0 0 0 3px rgba(16,185,129,.2); }
.dot.err { background: var(--err); box-shadow: 0 0 0 3px rgba(239,68,68,.2); }
.dot.warn{ background: var(--warn);box-shadow: 0 0 0 3px rgba(245,158,11,.2); }

/* file row in sidebar */
.file-row {
  display:flex; align-items:center; gap:8px; padding:7px 10px; margin-bottom:6px;
  border:1px solid var(--border); border-radius:10px; font-size:13px; background: var(--card);
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}

/* ── Hero ─────────────────────────────────────── */
.hero {
  position:relative; overflow:hidden; border-radius:20px; padding:30px 34px; margin-bottom:22px; color:#fff;
  background: radial-gradient(1200px 300px at 85% -20%, rgba(255,255,255,.22), transparent 60%),
              linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #c026d3 100%);
  box-shadow: 0 18px 40px rgba(99,102,241,.28);
}
.hero h1 { margin:0 0 6px; font-size:30px; font-weight:800; letter-spacing:-.6px; color:#fff; }
.hero p  { margin:0; font-size:15px; opacity:.88; max-width:640px; }
.hero .badges { margin-top:16px; display:flex; gap:8px; flex-wrap:wrap; }
.hero .badge {
  background: rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.28);
  padding:4px 12px; border-radius:999px; font-size:12px; font-weight:600; backdrop-filter: blur(6px);
}

/* ── Stat cards ─────────────────────────────────────── */
.stat {
  border:1px solid var(--border); border-radius:16px; padding:16px 18px; background: var(--card);
  transition: transform .15s ease, box-shadow .15s ease;
}
.stat:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(0,0,0,.08); }
.stat .lbl { font-size:12px; font-weight:600; opacity:.6; text-transform:uppercase; letter-spacing:.06em; }
.stat .val { font-size:28px; font-weight:800; letter-spacing:-.5px; margin-top:2px; }
.stat .ico { float:right; font-size:20px; background: var(--brand-soft); border-radius:10px; padding:6px 9px; }

/* ── Section titles / cards ─────────────────────── */
.section-title { font-size:18px; font-weight:700; letter-spacing:-.2px; margin: 4px 0 2px; }
.section-sub   { font-size:13.5px; opacity:.62; margin-bottom:14px; }
.card {
  border:1px solid var(--border); border-radius:16px; padding:18px 20px; background: var(--card); margin-bottom:14px;
}
.step {
  display:flex; gap:12px; align-items:flex-start; padding:10px 0;
}
.step .n {
  min-width:28px; height:28px; border-radius:50%; display:grid; place-items:center;
  background: var(--brand-soft); color: var(--brand); font-weight:800; font-size:13px;
}
.step b { font-size:14px; } .step span { font-size:13px; opacity:.65; display:block; }

/* ── Tabs ─────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  gap:6px; background: var(--card); padding:5px; border-radius:14px; border:1px solid var(--border); width:fit-content;
}
.stTabs [data-baseweb="tab"] {
  height:42px; padding:0 22px; border-radius:10px; font-weight:600; font-size:14.5px; background:transparent;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--brand), var(--brand-2)) !important; color:#fff !important;
  box-shadow: 0 6px 16px rgba(99,102,241,.35);
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display:none; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 22px; }

/* ── Buttons ─────────────────────────────────────── */
.stButton > button, .stDownloadButton > button {
  border-radius:11px; font-weight:600; border:1px solid var(--border); transition: all .15s ease;
}
.stButton > button:hover { border-color: var(--brand); color: var(--brand); transform: translateY(-1px); }
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, var(--brand), var(--brand-2)); color:#fff; border:none;
  box-shadow: 0 8px 20px rgba(99,102,241,.35); padding:.6rem 1.4rem;
}
.stButton > button[kind="primary"]:hover { color:#fff; box-shadow: 0 12px 26px rgba(99,102,241,.45); }

/* ── Uploader ─────────────────────────────────────── */
[data-testid="stFileUploaderDropzone"] {
  border:2px dashed rgba(99,102,241,.45); border-radius:18px; background: var(--brand-soft); padding:28px;
}
[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--brand); }

/* ── Chat ─────────────────────────────────────── */
[data-testid="stChatMessage"] {
  border:1px solid var(--border); border-radius:16px; padding:14px 18px; background: var(--card); margin-bottom:12px;
}
[data-testid="stChatInput"] { border-radius:16px; border:1px solid var(--border); }
.empty {
  text-align:center; padding:36px 10px 14px;
}
.empty .big { font-size:42px; }
.empty h3 { margin:6px 0 4px; font-weight:700; letter-spacing:-.3px; }
.empty p  { opacity:.6; font-size:14px; }

/* ── Misc ─────────────────────────────────────── */
[data-testid="stExpander"] { border:1px solid var(--border); border-radius:14px; background: transparent; }
hr { border-color: var(--border) !important; }
.src-chip {
  display:inline-block; padding:2px 10px; border-radius:999px; font-size:12px; font-weight:600;
  background: var(--brand-soft); color: var(--brand); margin-right:6px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "messages": [], "chunks": [], "doc_names": [],
    "bm25_index": None, "indexed": False, "prefill": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

MODELS = ["openai/gpt-oss-20b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        """
<div class="brand">
  <div class="brand-logo">💠</div>
  <div><div class="brand-name">FinSight</div><div class="brand-sub">Financial RAG Assistant</div></div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-label">Status</div>', unsafe_allow_html=True)
    if KEY_OK:
        st.markdown('<span class="pill"><span class="dot ok"></span>Groq connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="pill"><span class="dot err"></span>API key missing</span>', unsafe_allow_html=True)
        st.caption("Add `GROQ_API_KEY=gsk_...` to the `.env` file in the project root, then restart. "
                   "Free key: console.groq.com")

    st.markdown('<div class="side-label">Model</div>', unsafe_allow_html=True)
    model = st.selectbox("Model", MODELS, label_visibility="collapsed")

    st.markdown('<div class="side-label">Retrieval settings</div>', unsafe_allow_html=True)
    top_k         = st.slider("Top K chunks", 1, 15, 5)
    chunk_size    = st.slider("Chunk size", 200, 2000, 500, 100)
    chunk_overlap = st.slider("Chunk overlap", 0, 300, 50, 25)
    show_sources  = st.toggle("Show source excerpts", value=True)

    if st.session_state.doc_names:
        st.markdown('<div class="side-label">Knowledge base</div>', unsafe_allow_html=True)
        for n in st.session_state.doc_names:
            st.markdown(f'<div class="file-row">📄 {n}</div>', unsafe_allow_html=True)
        st.caption(f"{len(st.session_state.chunks)} chunks indexed")

    st.markdown('<div class="side-label">Actions</div>', unsafe_allow_html=True)
    if st.session_state.messages:
        st.download_button(
            "⬇️ Export chat (JSON)",
            data=json.dumps(st.session_state.messages, indent=2, default=str),
            file_name="finsight_chat.json",
            mime="application/json",
            use_container_width=True,
        )
        if st.button("🧹 Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    if st.button("🗑️ Reset workspace", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chunks = []
        st.session_state.doc_names = []
        st.session_state.bm25_index = None
        st.session_state.indexed = False
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
<div class="hero">
  <h1>Ask your financial documents anything.</h1>
  <p>Upload annual reports, earnings calls and news. FinSight retrieves the exact passages and answers
     with figures, page numbers and sources — grounded only in your files.</p>
  <div class="badges">
    <span class="badge">⚡ Groq-powered</span>
    <span class="badge">🔎 BM25 retrieval</span>
    <span class="badge">📑 Source citations</span>
    <span class="badge">🔒 Local indexing</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


def stat_card(col, icon, label, value):
    col.markdown(
        f'<div class="stat"><span class="ico">{icon}</span>'
        f'<div class="lbl">{label}</div><div class="val">{value}</div></div>',
        unsafe_allow_html=True,
    )


s1, s2, s3, s4 = st.columns(4)
stat_card(s1, "📄", "Documents", len(st.session_state.doc_names))
stat_card(s2, "🧩", "Chunks", f"{len(st.session_state.chunks):,}")
stat_card(s3, "💬", "Questions", sum(1 for m in st.session_state.messages if m["role"] == "user"))
stat_card(s4, "✅", "Index", "Ready" if st.session_state.indexed else "Empty")
st.write("")

# ══════════════════════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def clean(text):
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.replace("\x00", "").strip()


def extract_pdf(file_bytes, filename):
    company = filename.replace(".pdf", "").split("_")[0]

    try:
        import pdfplumber
        pages = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                for table in page.extract_tables():
                    for row in table:
                        row_text = " | ".join([str(c) for c in row if c])
                        if row_text.strip():
                            text += "\n" + row_text
                text = clean(text)
                if text.strip():
                    pages.append({"text": text, "source": filename,
                                  "page": i + 1, "company": company, "type": "pdf"})
        if pages and sum(len(p["text"]) for p in pages) > 500:
            return pages
    except ImportError:
        pass

    import pypdf
    pages = []
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text(extraction_mode="layout") or ""
        except Exception:
            text = page.extract_text() or ""
        text = clean(text)
        if text.strip():
            pages.append({"text": text, "source": filename,
                          "page": i + 1, "company": company, "type": "pdf"})
    if pages and sum(len(p["text"]) for p in pages) > 500:
        return pages

    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    full_text = ""
    for i, page in enumerate(reader.pages):
        try:
            t = page.extract_text(extraction_mode="layout") or ""
        except Exception:
            t = page.extract_text() or ""
        if t.strip():
            full_text += f"\n\n[Page {i+1}]\n{t}"
    full_text = clean(full_text)
    if full_text.strip():
        return [{"text": full_text, "source": filename,
                 "page": 0, "company": company, "type": "pdf_full"}]
    return []


def extract_txt(file_bytes, filename):
    text = clean(file_bytes.decode("utf-8", errors="ignore"))
    return [{"text": text, "source": filename, "page": 1,
             "company": filename.split("_")[0], "type": "earnings_call"}]


def extract_csv(file_bytes, filename):
    import pandas as pd
    df = pd.read_csv(io.BytesIO(file_bytes))
    return [{"text": f"Headline: {row.get('headline', str(row.iloc[0]))}",
             "source": filename, "page": 1, "company": "news", "type": "market_news"}
            for _, row in df.iterrows()]


def make_chunks(pages, size=500, overlap=50):
    chunks = []
    for page in pages:
        text = page["text"]
        if not text.strip():
            continue
        paragraphs = re.split(r"\n\n+", text)
        current, idx = "", 0
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if len(current) + len(para) + 2 <= size:
                current = (current + "\n\n" + para).strip()
            else:
                if current.strip():
                    chunks.append({**page, "text": current.strip(), "chunk_idx": idx})
                    idx += 1
                    current = (current[-overlap:] + "\n\n" + para).strip() if overlap else para
                else:
                    for sent in re.split(r"(?<=[.!?])\s+", para):
                        if len(current) + len(sent) + 1 <= size:
                            current = (current + " " + sent).strip()
                        else:
                            if current.strip():
                                chunks.append({**page, "text": current.strip(), "chunk_idx": idx})
                                idx += 1
                            current = sent.strip()
        if current.strip():
            chunks.append({**page, "text": current.strip(), "chunk_idx": idx})
    return chunks


def build_bm25(chunks):
    from rank_bm25 import BM25Okapi
    return BM25Okapi([c["text"].lower().split() for c in chunks])


def bm25_retrieve(query, chunks, bm25_index, k=5):
    scores = bm25_index.get_scores(query.lower().split())
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
    top = [c for c, _ in ranked[:k]]
    if all(s < 0.01 for _, s in ranked[:k]):
        keywords = [w for w in query.lower().split() if len(w) > 3]
        fallback = sorted(
            [(c, sum(1 for kw in keywords if kw in c["text"].lower())) for c in chunks],
            key=lambda x: x[1], reverse=True,
        )
        top = [c for c, hits in fallback[:k] if hits > 0] or top
    return top


def generate_answer(question, chunks, api_key, model_name):
    from groq import Groq
    context = "\n\n---\n\n".join([
        f"[Source: {c['source']} | Page: {c.get('page','?')} | Company: {c['company']}]\n{c['text']}"
        for c in chunks
    ])
    prompt = f"""You are a Senior Financial Analyst and document expert.
Read the context carefully and answer the question thoroughly.

RULES:
1. Use ONLY the context below. Do not use outside knowledge.
2. If the answer IS in the context, give a detailed answer with exact figures.
3. If the answer is NOT in the context, say: "I could not find this in the uploaded documents."
4. Quote exact numbers and figures as they appear.
5. Mention the source document and page number.
6. Be detailed and professional.

Context:
{context}

Question: {question}

**Answer:**

**Key Insights:**

**Sources:**
"""
    resp = Groq(api_key=api_key).chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1500,
    )
    return resp.choices[0].message.content


def render_sources(sources):
    with st.expander(f"📄 Sources ({len(sources)})"):
        for s in sources:
            st.markdown(
                f'<span class="src-chip">{s["source"]}</span>'
                f'<span class="src-chip">Page {s.get("page","?")}</span>'
                f'<span class="src-chip">{s["company"]}</span>',
                unsafe_allow_html=True,
            )
            st.caption(s["excerpt"])
            st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2 = st.tabs(["📂  Documents", "💬  Ask AI"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — DOCUMENTS
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    left, right = st.columns([2.2, 1], gap="large")

    with left:
        st.markdown('<div class="section-title">Upload documents</div>'
                    '<div class="section-sub">PDF reports, TXT/MD transcripts or CSV news files. '
                    'Indexed instantly in your browser session.</div>', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Drop files here",
            type=["pdf", "txt", "csv", "md"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        if uploaded:
            for f in uploaded:
                st.markdown(
                    f'<div class="file-row">📄 <b>{f.name}</b> &nbsp;·&nbsp; '
                    f'{round(len(f.getvalue())/1024,1)} KB</div>',
                    unsafe_allow_html=True,
                )

            if st.button("🚀 Process & index files", type="primary"):
                all_pages, errors = [], []
                prog = st.progress(0, "Reading files...")

                for i, uf in enumerate(uploaded):
                    prog.progress((i + 0.3) / len(uploaded), f"Extracting {uf.name}...")
                    try:
                        raw = uf.read()
                        ext = os.path.splitext(uf.name)[1].lower()
                        if ext == ".pdf":
                            pages = extract_pdf(raw, uf.name)
                        elif ext in (".txt", ".md"):
                            pages = extract_txt(raw, uf.name)
                        elif ext == ".csv":
                            pages = extract_csv(raw, uf.name)
                        else:
                            errors.append(f"`{uf.name}`: unsupported")
                            continue

                        if not pages:
                            errors.append(f"`{uf.name}`: no text extracted — try converting to .txt")
                            continue

                        total = sum(len(p["text"]) for p in pages)
                        st.write(f"✅ `{uf.name}` — {len(pages)} page(s), **{total:,}** characters")

                        # replace any previous copy of this file
                        st.session_state.chunks = [c for c in st.session_state.chunks if c["source"] != uf.name]
                        all_pages.extend(pages)

                        dest = {".pdf": "annual_reports", ".txt": "earnings_calls",
                                ".md": "earnings_calls", ".csv": "market_news"}[ext]
                        save_dir = os.path.join(ROOT, "data", "raw", dest)
                        os.makedirs(save_dir, exist_ok=True)
                        with open(os.path.join(save_dir, uf.name), "wb") as fh:
                            fh.write(raw)
                        if uf.name not in st.session_state.doc_names:
                            st.session_state.doc_names.append(uf.name)
                        prog.progress((i + 1) / len(uploaded), f"{uf.name} done")
                    except Exception as e:
                        errors.append(f"`{uf.name}`: {e}")

                if all_pages:
                    total_chars = sum(len(p["text"]) for p in all_pages)
                    prog.progress(0.85, "Chunking...")
                    new_chunks = make_chunks(all_pages, chunk_size, chunk_overlap)
                    st.session_state.chunks.extend(new_chunks)
                    prog.progress(0.95, "Building BM25 index...")
                    st.session_state.bm25_index = build_bm25(st.session_state.chunks)
                    st.session_state.indexed = True
                    prog.empty()
                    st.success(
                        f"Indexed {total_chars:,} characters into "
                        f"{len(st.session_state.chunks)} chunks. Head to the **Ask AI** tab."
                    )
                    for e in errors:
                        st.error(e)
                    if len(st.session_state.chunks) < 10:
                        st.warning("Very few chunks. Install `pdfplumber` and re-upload, or convert the PDF to .txt.")
                    else:
                        st.balloons()
                else:
                    prog.empty()
                    for e in errors:
                        st.error(e)

    with right:
        st.markdown(
            """
<div class="card">
  <div class="section-title">How it works</div>
  <div class="step"><div class="n">1</div><div><b>Upload</b><span>Add your filings & transcripts</span></div></div>
  <div class="step"><div class="n">2</div><div><b>Index</b><span>Text is chunked and BM25-indexed</span></div></div>
  <div class="step"><div class="n">3</div><div><b>Ask</b><span>Get cited, grounded answers</span></div></div>
</div>
""",
            unsafe_allow_html=True,
        )
        with st.expander("💡 Better PDF extraction"):
            st.code("pip install pdfplumber", language="bash")
            st.caption("Handles tables and multi-column layouts. Restart the app after installing.")
        with st.expander("ℹ️ Supported formats"):
            st.markdown(
                "| Format | Purpose |\n|---|---|\n"
                "| `.pdf` | Annual reports, statements |\n"
                "| `.txt` `.md` | Earnings calls, notes |\n"
                "| `.csv` | News (`headline,date`) |"
            )

    st.markdown("---")
    st.markdown('<div class="section-title">Indexed documents</div>', unsafe_allow_html=True)

    if not st.session_state.doc_names:
        st.info("No documents yet. Upload files above to get started.")
    else:
        for name in list(st.session_state.doc_names):
            n_chunks = sum(1 for c in st.session_state.chunks if c["source"] == name)
            ca, cb, cc = st.columns([6, 1.6, 1])
            ca.markdown(f'<div class="file-row">📄 <b>{name}</b></div>', unsafe_allow_html=True)
            cb.markdown(f'<span class="pill">{n_chunks} chunks</span>', unsafe_allow_html=True)
            if cc.button("🗑️", key=f"del_{name}", help="Remove this document"):
                st.session_state.doc_names.remove(name)
                st.session_state.chunks = [c for c in st.session_state.chunks if c["source"] != name]
                st.session_state.bm25_index = (
                    build_bm25(st.session_state.chunks) if st.session_state.chunks else None
                )
                st.session_state.indexed = bool(st.session_state.chunks)
                st.rerun()

        if st.session_state.chunks:
            with st.expander("🔍 Preview extracted chunks"):
                for i, chunk in enumerate(st.session_state.chunks[:5]):
                    st.markdown(
                        f'<span class="src-chip">Chunk {i+1}</span>'
                        f'<span class="src-chip">{chunk["source"]}</span>'
                        f'<span class="src-chip">Page {chunk.get("page","?")}</span>',
                        unsafe_allow_html=True,
                    )
                    st.caption(chunk["text"][:300] + "...")
                    st.divider()

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — CHAT
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    if not KEY_OK:
        st.error("Groq API key not found in `.env`.")
        st.markdown(
            "1. Open `financial-rag-system/.env`\n"
            "2. Add `GROQ_API_KEY=gsk_your_actual_key_here`\n"
            "3. Get a free key at https://console.groq.com\n"
            "4. Save and restart the app"
        )
        st.stop()

    if not st.session_state.indexed:
        st.markdown(
            '<div class="empty"><div class="big">📭</div><h3>No documents indexed yet</h3>'
            '<p>Upload and index files in the <b>Documents</b> tab to start asking questions.</p></div>',
            unsafe_allow_html=True,
        )
        st.stop()

    # Empty state with suggestion chips
    if not st.session_state.messages:
        st.markdown(
            '<div class="empty"><div class="big">💬</div><h3>What would you like to know?</h3>'
            '<p>Try one of these, or type your own question below.</p></div>',
            unsafe_allow_html=True,
        )
        suggestions = [
            "What was total revenue?",
            "What was net income?",
            "What were the key risk factors?",
            "What was earnings per share?",
            "What are the debt obligations?",
            "What was the operating margin?",
            "Summarize the document",
            "What is this document about?",
            "What are the main features?",
        ]
        cols = st.columns(3)
        for i, s in enumerate(suggestions):
            if cols[i % 3].button(s, use_container_width=True, key=f"sq_{i}"):
                st.session_state.prefill = s
                st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑‍💼" if msg["role"] == "user" else "💠"):
            st.markdown(msg["content"])
            if msg.get("sources") and show_sources:
                render_sources(msg["sources"])

    prefill = st.session_state.get("prefill", "")
    if prefill:
        st.session_state.prefill = ""

    question = st.chat_input("Ask a financial question about your documents...") or prefill

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user", avatar="🧑‍💼"):
            st.markdown(question)
        with st.chat_message("assistant", avatar="💠"):
            with st.spinner("Searching documents and generating answer..."):
                try:
                    top_chunks = bm25_retrieve(question, st.session_state.chunks,
                                               st.session_state.bm25_index, k=top_k)
                    answer = generate_answer(question, top_chunks, GROQ_API_KEY, model)
                    sources = [{"source": c["source"], "company": c["company"],
                                "page": c.get("page", "?"), "excerpt": c["text"][:300]}
                               for c in top_chunks]
                    st.markdown(answer)
                    if sources and show_sources:
                        render_sources(sources)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer, "sources": sources})
                except Exception as e:
                    err = f"❌ Error: {e}"
                    st.error(err)
                    if "401" in str(e) or "auth" in str(e).lower():
                        st.info("Check your GROQ_API_KEY in the .env file.")
                    elif "429" in str(e):
                        st.info("Rate limit reached — wait a few seconds and try again.")
                    elif "model" in str(e).lower():
                        st.info("This model may be unavailable — pick another one in the sidebar.")
                    st.session_state.messages.append({"role": "assistant", "content": err})