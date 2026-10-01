import html
import streamlit as st

from config import get_groq_api_key
from resume_parser import extract_resume_text
from groq_analyzer import analyze_resume


st.set_page_config(
    page_title=" AI Resume Analyzer",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 8% 8%, rgba(255, 155, 207, .30), transparent 28%),
        radial-gradient(circle at 92% 18%, rgba(255, 105, 180, .20), transparent 28%),
        linear-gradient(135deg, #fff9fc 0%, #ffeaf5 48%, #fff 100%);
    font-family: 'Inter', sans-serif;
}
.block-container { max-width: 1200px; padding-top: 2rem; padding-bottom: 4rem; }

.hero, .glass-card {
    border: 1px solid rgba(255,255,255,.78);
    background: rgba(255,255,255,.52);
    box-shadow: 0 18px 55px rgba(177,49,112,.11);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
}
.hero { padding: 2rem 2.2rem; border-radius: 28px; margin-bottom: 1.5rem; }
.hero h1 { margin: 0; color: #92245d; font-size: 2.55rem; font-weight: 800; letter-spacing: -1px; }
.hero p { color: #705567; margin: .6rem 0 0; }

.glass-card { padding: 1.25rem 1.4rem; border-radius: 22px; margin-bottom: 1rem; }
.section-title { color: #92245d; font-size: 1.1rem; font-weight: 800; margin-bottom: .65rem; }
.muted { color: #806878; line-height: 1.65; }

.score-card {
    text-align:center; padding:1.55rem; border-radius:24px;
    background:linear-gradient(135deg,rgba(255,255,255,.78),rgba(255,220,238,.68));
    border:1px solid rgba(255,255,255,.9);
    box-shadow:0 15px 45px rgba(177,49,112,.14);
}
.score { font-size:4rem; line-height:1; font-weight:800; color:#d62d7b; }
.score-label { color:#77586a; margin-top:.55rem; font-weight:650; }

.pill {
    display:inline-block; padding:.38rem .68rem; margin:.22rem .18rem;
    border-radius:999px; background:rgba(255,228,242,.9);
    border:1px solid rgba(214,45,123,.14); color:#8e2459;
    font-size:.86rem; font-weight:650;
}
.pill-green { background:rgba(227,250,238,.88); color:#176b43; border-color:rgba(23,107,67,.12); }
.pill-red { background:rgba(255,233,238,.92); color:#a1264f; border-color:rgba(161,38,79,.12); }

div[data-testid="stFileUploaderDropzone"] {
    background:rgba(255,255,255,.48); border:1px dashed rgba(214,45,123,.35); border-radius:18px;
}
.stTextArea textarea { background:rgba(255,255,255,.58) !important; border-radius:18px !important; }
.stButton > button {
    width:100%; border:0; border-radius:15px; padding:.78rem 1rem;
    background:linear-gradient(90deg,#d62d7b,#f05a9b); color:white;
    font-weight:800; box-shadow:0 10px 24px rgba(214,45,123,.24);
}
.stButton > button:hover { background:linear-gradient(90deg,#c4246d,#e84b91); color:white; }
.footer { text-align:center; color:#8c7080; font-size:.82rem; margin-top:2rem; }
</style>
""", unsafe_allow_html=True)


def render_pills(items, css_class=""):
    if not items:
        st.markdown('<span class="muted">None identified.</span>', unsafe_allow_html=True)
        return
    output = []
    for item in items:
        output.append(
            f'<span class="pill {css_class}">{html.escape(str(item))}</span>'
        )
    st.markdown("".join(output), unsafe_allow_html=True)


def render_list(items):
    if not items:
        st.markdown('<span class="muted">None identified.</span>', unsafe_allow_html=True)
        return
    for item in items:
        st.markdown(f"- {html.escape(str(item))}")


st.markdown("""
<div class="hero">
    <h1>💗 PinkCV AI Resume Analyzer</h1>
    <p>Compare your resume with a job description using Groq AI and discover your match score, ATS keywords, skill gaps, resume problems, and practical recommendations.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-title">📄 1. Upload your resume</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader(
        "Choose a PDF resume",
        type=["pdf"],
        help="Use a text-based PDF. Scanned/image-only PDFs may not contain extractable text.",
    )

with right:
    st.markdown('<div class="section-title">📝 2. Paste the job description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job description",
        height=250,
        placeholder="Paste the complete job description here...",
        label_visibility="collapsed",
    )

st.markdown("")
analyze_clicked = st.button("✨ Analyze My Resume", use_container_width=True)

if analyze_clicked:
    if not resume_file:
        st.error("Please upload your resume PDF.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste the job description.")
        st.stop()

    try:
        api_key = get_groq_api_key()
    except RuntimeError as exc:
        st.error(str(exc))
        st.stop()

    with st.spinner("Reading your resume..."):
        try:
            resume_text = extract_resume_text(resume_file.getvalue())
        except Exception as exc:
            st.error(f"Could not read the PDF: {exc}")
            st.stop()

    if len(resume_text.strip()) < 80:
        st.error("Very little text could be extracted. Please use a text-based PDF or export the resume again as PDF.")
        st.stop()

    with st.spinner("Groq is comparing your resume with the job description..."):
        try:
            st.session_state["analysis"] = analyze_resume(
                resume_text=resume_text,
                job_description=job_description.strip(),
                api_key=api_key,
            )
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")
            st.stop()

result = st.session_state.get("analysis")

if result:
    st.markdown("---")
    st.markdown('<div class="section-title">📊 Analysis Results</div>', unsafe_allow_html=True)

    score_col, summary_col = st.columns([1, 2], gap="large")
    with score_col:
        st.markdown(
            f'<div class="score-card"><div class="score">{result["match_score"]}%</div><div class="score-label">Overall Resume Match</div></div>',
            unsafe_allow_html=True,
        )

    with summary_col:
        st.markdown(
            f'<div class="glass-card"><div class="section-title">📋 Final Result</div><div class="muted">{html.escape(result["final_result"])}</div></div>',
            unsafe_allow_html=True,
        )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="glass-card"><div class="section-title">✅ Matching Skills</div>', unsafe_allow_html=True)
        render_pills(result["matching_skills"], "pill-green")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass-card"><div class="section-title">❌ Missing Skills</div>', unsafe_allow_html=True)
        render_pills(result["missing_skills"], "pill-red")
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2, gap="large")
    with c3:
        st.markdown('<div class="glass-card"><div class="section-title">🔑 ATS Keywords Found</div>', unsafe_allow_html=True)
        render_pills(result["ats_keywords"]["found"], "pill-green")
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="glass-card"><div class="section-title">🔎 ATS Keywords Missing</div>', unsafe_allow_html=True)
        render_pills(result["ats_keywords"]["missing"], "pill-red")
        st.markdown("</div>", unsafe_allow_html=True)

    c5, c6 = st.columns(2, gap="large")
    with c5:
        st.markdown('<div class="glass-card"><div class="section-title">⚠️ Resume Problems</div>', unsafe_allow_html=True)
        render_list(result["resume_problems"])
        st.markdown("</div>", unsafe_allow_html=True)
    with c6:
        st.markdown('<div class="glass-card"><div class="section-title">💡 Recommendations</div>', unsafe_allow_html=True)
        render_list(result["recommendations"])
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="footer">AI-generated analysis is guidance, not a guarantee of ATS screening or hiring outcomes.</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="glass-card">
        <div class="section-title">🚀 How it works</div>
        <div class="muted">Upload your PDF → paste the job description → click Analyze → review your match score, skills, ATS keywords, resume problems, and recommendations.</div>
    </div>
    """, unsafe_allow_html=True)
