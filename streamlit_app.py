"""
Summarize AI - Streamlit Web App
Full-featured UI: Home, Library, Projects, Settings, Help
"""

import streamlit as st
import json
import os
from datetime import datetime
from app import extractive_summarize, fetch_url_text

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Summarize AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Data persistence ────────────────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), "app_data.json")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "library": [],
        "projects": [],
        "settings": {
            "username": "User",
            "default_length": "Medium",
            "default_tone": "Professional",
        }
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── CSS ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ═══════════════════════════════════════════════════════
   RULE 1 — Main content: WHITE background → DARK text
   ═══════════════════════════════════════════════════════ */
.main .block-container,
.main .block-container * {
    color: #111827;
    font-family: 'Inter', sans-serif !important;
}

/* Page background */
.stApp { background: #eef0f8 !important; }
#MainMenu, footer, header { visibility: hidden; }

/* Markdown body text */
.stMarkdown p  { color: #374151 !important; }
.stMarkdown li { color: #374151 !important; }
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3 { color: #111827 !important; }

/* Widget labels in main content */
.main .stTextInput   > label,
.main .stTextArea    > label,
.main .stSelectbox   > label,
.main .stSlider      > label,
.main .stSelectSlider > label,
.main .stRadio       > label,
.main .stCheckbox    > label,
.main .stNumberInput > label {
    color: #374151 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* Metric widget */
[data-testid="stMetric"] label    { color: #6b7280 !important; font-size: 12px !important; }
[data-testid="stMetricValue"]     { color: #111827 !important; font-weight: 700 !important; }

/* Expander headers */
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span { color: #111827 !important; font-weight: 600 !important; }

/* Select slider value */
[data-testid="stSelectSlider"] p  { color: #374151 !important; }
.stSlider p                       { color: #374151 !important; }

/* Radio option labels */
[data-testid="stRadio"] > div > label,
[data-testid="stRadio"] > div > label span { color: #374151 !important; }

/* Alerts keep their own colour */
[data-testid="stAlert"] p { color: inherit !important; }

/* Toast (dark pill — keep white) */
[data-testid="stToast"] p { color: white !important; }

/* Caption */
.stCaption, .stCaption p { color: #9ca3af !important; font-size: 12px !important; }

/* ═══════════════════════════════════════════════════════
   RULE 2 — Sidebar: DARK (#111827) background → LIGHT text
   ═══════════════════════════════════════════════════════ */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] *,
[data-testid="stSidebarContent"],
[data-testid="stSidebarContent"] * {
    color: #9ca3af !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Sidebar sizing ── */
section[data-testid="stSidebar"][aria-expanded="true"] {
    min-width: 108px !important;
    max-width: 108px !important;
    background-color: #111827 !important;
}
section[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
    width: 108px !important;
    background-color: #111827 !important;
}
[data-testid="stSidebarContent"] {
    background-color: #111827 !important;
    padding: 18px 8px !important;
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* ── Sidebar nav buttons ── */
[data-testid="stSidebar"] .stButton button {
    width: 80px !important;
    height: 58px !important;
    background: transparent !important;
    border: none !important;
    border-radius: 14px !important;
    font-size: 16px !important;
    flex-direction: column !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 3px !important;
    margin: 3px auto !important;
    padding: 6px 0 !important;
    box-shadow: none !important;
    color: #9ca3af !important;
    transition: background 0.18s, color 0.18s !important;
    line-height: 1.2 !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255,255,255,0.1) !important;
    color: #f9fafb !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── Collapse chevron (visible on dark bg) ── */
[data-testid="stSidebar"] button[title="Collapse sidebar"],
[data-testid="stSidebar"] button[kind="header"] {
    color: #6b7280 !important;
    background: transparent !important;
    border: none !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] button[title="Collapse sidebar"]:hover {
    color: white !important;
    background: rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
}

/* ── Expand tab (shown when sidebar is collapsed) ── */
[data-testid="collapsedControl"] button {
    background: linear-gradient(180deg, #4361ee, #7c3aed) !important;
    border: none !important;
    border-radius: 0 8px 8px 0 !important;
    color: white !important;
    box-shadow: 2px 0 12px rgba(67,97,238,0.45) !important;
}

/* ═══════════════════════════════════════════════════════
   RULE 3 — Gradient / coloured buttons → WHITE text
   ═══════════════════════════════════════════════════════ */
.sum-btn  .stButton button,
.save-btn .stButton button {
    color: white !important;
}


    background: transparent !important;
    border: none !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] button[title="Collapse sidebar"]:hover {
    color: white !important;
    background: rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
}
/* Expand tab (shown when collapsed) */
[data-testid="collapsedControl"] button {
    background: linear-gradient(180deg, #4361ee, #7c3aed) !important;
    border: none !important;
    border-radius: 0 8px 8px 0 !important;
    color: white !important;
    box-shadow: 2px 0 12px rgba(67,97,238,0.45) !important;
}

/* ── Main content area ── */
.block-container {
    padding: 28px 36px 28px 28px !important;
    max-width: 100% !important;
}

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
}
.topbar-title {
    font-size: 24px;
    font-weight: 800;
    color: #111827;
    letter-spacing: -0.5px;
    margin: 0;
}
.topbar-sub {
    font-size: 13px;
    color: #9ca3af;
    margin: 3px 0 0 0;
}
.tb-right {
    display: flex;
    align-items: center;
    gap: 10px;
}
.tb-search {
    background: white;
    border: 1.5px solid #e5e7eb;
    border-radius: 10px;
    padding: 9px 16px;
    font-size: 13px;
    color: #9ca3af;
    width: 200px;
    display: inline-block;
}

/* ── Cards ── */
.card {
    background: white;
    border-radius: 18px;
    padding: 22px 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    margin-bottom: 18px;
}
.card-title { font-size: 15px; font-weight: 700; color: #111827; }
.card-sub   { font-size: 13px; color: #9ca3af; margin-top: 2px; }
.card-hdr   {
    display: flex; align-items: center;
    justify-content: space-between; margin-bottom: 16px;
}
.dots { color: #d1d5db; font-size: 18px; letter-spacing: 2px; }

/* ── Stat chips ── */
.stat-row { display: flex; gap: 12px; margin-bottom: 18px; }
.stat-chip {
    background: white; border-radius: 14px;
    padding: 16px 20px; flex: 1;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.stat-val   { font-size: 24px; font-weight: 800; color: #111827; }
.stat-label { font-size: 12px; color: #9ca3af; margin-top: 2px; }

/* ── Option label ── */
.opt-label {
    font-size: 11px; font-weight: 700; color: #9ca3af;
    text-transform: uppercase; letter-spacing: 0.7px; margin-bottom: 8px;
}

/* ── Textarea ── */
.stTextArea textarea {
    border: 1.5px solid #e5e7eb !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    color: #374151 !important;
    line-height: 1.75 !important;
    resize: none !important;
    background: #f9fafb !important;
    padding: 14px !important;
}
.stTextArea textarea:focus {
    border-color: #4361ee !important;
    box-shadow: 0 0 0 3px rgba(67,97,238,0.12) !important;
    background: white !important;
}
[data-testid="stTextArea"] label { display: none !important; }

/* ── Text input ── */
.stTextInput input {
    border: 1.5px solid #e5e7eb !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    color: #374151 !important;
    background: #f9fafb !important;
    padding: 10px 14px !important;
}
.stTextInput input:focus {
    border-color: #4361ee !important;
    box-shadow: 0 0 0 3px rgba(67,97,238,0.12) !important;
    background: white !important;
}
[data-testid="stTextInput"] label { display: none !important; }

/* ── Selectbox — all text must be dark ── */
[data-testid="stSelectbox"] label { display: none !important; }
[data-testid="stSelectbox"] > div > div {
    border: 1.5px solid #e5e7eb !important;
    border-radius: 11px !important;
    background: white !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #374151 !important;
}
/* Target every text node inside the selectbox widget */
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p,
[data-testid="stSelectbox"] div {
    color: #374151 !important;
}
/* Override any white-text leak from sidebar * rule */
.main [data-testid="stSelectbox"] *,
.block-container [data-testid="stSelectbox"] * {
    color: #374151 !important;
}

/* ── Select slider ── */
[data-testid="stSelectSlider"] label { display: none !important; }
[data-testid="stSelectSlider"] .stSlider div { color: #374151 !important; }

/* ── Radio ── */
[data-testid="stRadio"] label { display: none !important; }
[data-testid="stRadio"] > div {
    background: #f3f4f6;
    border-radius: 10px;
    padding: 4px;
    gap: 4px !important;
}
[data-testid="stRadio"] > div > label {
    display: flex !important;
    border-radius: 8px !important;
    padding: 6px 14px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #374151 !important;
}

/* ── Word count ── */
.wc { font-size: 13px; color: #9ca3af; margin-top: 8px; font-weight: 500; }

/* ── SUMMARIZE button ── */
.sum-btn .stButton button {
    background: linear-gradient(135deg, #4361ee 0%, #7c3aed 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 13px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 14px 24px !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(67,97,238,0.4) !important;
    transition: all 0.22s !important;
}
.sum-btn .stButton button:hover {
    box-shadow: 0 8px 28px rgba(67,97,238,0.55) !important;
    transform: translateY(-2px) !important;
}

/* ── Save settings button ── */
.save-btn .stButton button {
    background: linear-gradient(135deg, #4361ee 0%, #7c3aed 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 13px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    width: 100% !important;
    box-shadow: 0 4px 16px rgba(67,97,238,0.35) !important;
    transition: all 0.22s !important;
}

/* ── Small action buttons ── */
.act .stButton button {
    background: #f3f4f6 !important;
    color: #374151 !important;
    border: 1.5px solid #e5e7eb !important;
    border-radius: 9px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 7px 12px !important;
    box-shadow: none !important;
    transition: all 0.15s !important;
}
.act .stButton button:hover {
    background: #ede9fe !important;
    color: #4361ee !important;
    border-color: #a5b4fc !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Download button */
.act .stDownloadButton button {
    background: #f3f4f6 !important;
    color: #374151 !important;
    border: 1.5px solid #e5e7eb !important;
    border-radius: 9px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 7px 12px !important;
    box-shadow: none !important;
}
.act .stDownloadButton button:hover {
    background: #ede9fe !important;
    color: #4361ee !important;
    border-color: #a5b4fc !important;
}

/* ── Summary bullets ── */
.s-title { font-size: 17px; font-weight: 800; color: #111827; margin-bottom: 2px; }
.s-sub   { font-size: 13px; color: #9ca3af; margin-bottom: 16px; }
.blt {
    display: flex; gap: 10px; align-items: flex-start;
    background: #f5f7ff;
    border-left: 3px solid #4361ee;
    border-radius: 11px; padding: 12px 14px;
    margin-bottom: 10px; font-size: 14px;
    color: #374151; line-height: 1.68;
}
.blt-n {
    background: linear-gradient(135deg, #4361ee, #7c3aed);
    color: white; border-radius: 50%;
    width: 22px; height: 22px; min-width: 22px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 800; margin-top: 2px; flex-shrink: 0;
}
.s-footer {
    border-top: 1px solid #f3f4f6; margin-top: 14px;
    padding-top: 12px; font-size: 13px;
    color: #9ca3af; font-weight: 500;
}

/* ── Library / Project cards ── */
.lib-card {
    background: #f8f9ff; border-radius: 12px;
    padding: 16px 18px; margin-bottom: 10px;
    border-left: 4px solid #4361ee;
}
.lib-title  { font-size: 14px; font-weight: 700; color: #111827; margin-bottom: 3px; }
.lib-meta   { font-size: 12px; color: #9ca3af; margin-bottom: 6px; }
.lib-preview{ font-size: 13px; color: #6b7280; line-height: 1.6; }

/* ── Help ── */
.help-item  { display: flex; gap: 14px; padding: 16px 0; border-bottom: 1px solid #f3f4f6; }
.help-icon  { font-size: 22px; width: 34px; text-align: center; flex-shrink: 0; }
.help-title { font-size: 14px; font-weight: 700; color: #111827; margin-bottom: 4px; }
.help-desc  { font-size: 13px; color: #6b7280; line-height: 1.6; }

/* ── Empty state ── */
.empty-wrap {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-height: 260px; text-align: center; gap: 10px; padding: 30px 0;
}
.empty-ico  { font-size: 42px; }
.empty-ttl  { font-size: 15px; font-weight: 700; color: #9ca3af; }
.empty-hint { font-size: 13px; color: #c4c9d4; }

/* ── Alerts ── */
[data-testid="stAlert"] { border-radius: 12px !important; }

/* ── Sidebar logo ── */
.sb-logo {
    background: linear-gradient(135deg, #4361ee, #7c3aed);
    color: white;
    width: 46px; height: 46px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 800;
    margin: 0 auto 24px auto;
    box-shadow: 0 4px 14px rgba(67,97,238,0.45);
}
</style>
""", unsafe_allow_html=True)

# ── Auto-expand sidebar ONCE per browser session (using sessionStorage guard) ──
st.markdown("""
<script>
(function() {
  // Only auto-expand once per browser session, not on every Streamlit rerun
  if (!window.sessionStorage.getItem('sb_expanded')) {
    window.sessionStorage.setItem('sb_expanded', '1');
    setTimeout(function() {
      var btn = window.parent.document.querySelector(
        '[data-testid="collapsedControl"] button'
      );
      if (btn) { btn.click(); }
    }, 400);
  }
})();
</script>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def ss(key, val):
    if key not in st.session_state:
        st.session_state[key] = val

app_data = load_data()

# ── Session state ──────────────────────────────────────────────────────────────
ss("nav_page",       "Home")
ss("summary",        [])
ss("summary_text",   "")
ss("original_words", 0)
ss("last_reduction", 0)
ss("current_length", app_data["settings"].get("default_length", "Medium"))
ss("current_tone",   app_data["settings"].get("default_tone", "Professional"))
ss("proj_open",      False)

# ── Sidebar ────────────────────────────────────────────────────────────────────
NAV = [("🏠", "Home"), ("📚", "Library"), ("📁", "Projects"), ("⚙️", "Settings"), ("❓", "Help")]

with st.sidebar:
    st.markdown("<div class='sb-logo'>✦</div>", unsafe_allow_html=True)
    for icon, label in NAV:
        if st.button(f"{icon}\n{label}", key=f"nav_{label}", help=label):
            st.session_state.nav_page = label
            st.rerun()

page = st.session_state.nav_page

# ── Topbar ─────────────────────────────────────────────────────────────────────
PAGE_META = {
    "Home":     ("Welcome, " + app_data["settings"].get("username","User") + "! 👋",
                 "Summarize any text or article instantly"),
    "Library":  ("📚 Library",   "All your saved summaries"),
    "Projects": ("📁 Projects",  "Organize summaries into projects"),
    "Settings": ("⚙️ Settings",  "Customize your experience"),
    "Help":     ("❓ Help & Guide", "Learn how to use Summarize AI"),
}
ttl, sub = PAGE_META.get(page, ("Summarize AI", ""))

st.markdown(f"""
<div class="topbar">
  <div>
    <p class="topbar-title">{ttl}</p>
    <p class="topbar-sub">{sub}</p>
  </div>
  <div class="tb-right">
    <span class="tb-search">🔍 &nbsp;Search...</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# HOME
# ════════════════════════════════════════════════════════════════════════════════
if page == "Home":
    # Stats
    lib   = app_data["library"]
    n_lib = len(lib)
    n_pro = len(app_data["projects"])
    avg_r = round(sum(x.get("reduction",0) for x in lib) / n_lib, 1) if n_lib else 0

    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-chip">
        <div class="stat-val">{n_lib}</div>
        <div class="stat-label">Summaries Saved</div>
      </div>
      <div class="stat-chip">
        <div class="stat-val">{n_pro}</div>
        <div class="stat-label">Projects</div>
      </div>
      <div class="stat-chip">
        <div class="stat-val">{avg_r}%</div>
        <div class="stat-label">Avg. Reduction</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Options row
    LENGTH_MAP = {"Short": 2, "Medium": 4, "Long": 7}
    TONE_LIST  = ["Professional", "Casual", "Academic", "Creative"]

    oc1, oc2 = st.columns([2.2, 1])
    with oc1:
        st.markdown("<div class='card' style='margin-bottom:18px;'><div class='opt-label'>Summary Length</div>", unsafe_allow_html=True)
        length_val = st.select_slider("Length",
            options=["Short","Medium","Long"],
            value=st.session_state.current_length,
            key="length_slider", label_visibility="collapsed")
        st.session_state.current_length = length_val
        num_sentences = LENGTH_MAP[length_val]
        st.markdown("</div>", unsafe_allow_html=True)

    with oc2:
        st.markdown("<div class='card' style='margin-bottom:18px;'><div class='opt-label'>Tone</div>", unsafe_allow_html=True)
        tone = st.selectbox("Tone", TONE_LIST,
            index=TONE_LIST.index(st.session_state.current_tone),
            key="tone_select", label_visibility="collapsed")
        st.session_state.current_tone = tone
        st.markdown("</div>", unsafe_allow_html=True)

    # Two columns
    lc, rc = st.columns([1.05, 1], gap="large")

    # ── Left: Input ────────────────────────────────────────────────────────────
    with lc:
        st.markdown("""
        <div class="card">
          <div class="card-hdr">
            <div>
              <div class="card-title">Paste Original Text</div>
              <div class="card-sub">Enter text or fetch from a URL</div>
            </div>
            <div class="dots">···</div>
          </div>
        </div>""", unsafe_allow_html=True)

        mode = st.radio("Input mode",
            ["📄 Text Input", "🌐 URL"],
            horizontal=True, label_visibility="collapsed", key="input_mode")

        text_input = ""

        if mode == "📄 Text Input":
            text_input = st.text_area("Text", height=270,
                placeholder="Paste your article, essay, or any long text here…\nThe AI extracts the most important sentences automatically.",
                key="text_area_input", label_visibility="collapsed")
        else:
            url_val = st.text_input("URL", placeholder="https://example.com/article",
                key="url_input", label_visibility="collapsed")
            if url_val:
                with st.spinner("Fetching content…"):
                    try:
                        text_input = fetch_url_text(url_val)
                        st.success(f"✅ Fetched {len(text_input):,} characters")
                        with st.expander("Preview"):
                            st.write(text_input[:700] + "…" if len(text_input) > 700 else text_input)
                    except Exception as e:
                        st.error(f"❌ {e}")

        words = len(text_input.split()) if text_input.strip() else 0
        chars = len(text_input)
        st.markdown(f"<div class='wc'>{words:,} words &nbsp;/&nbsp; {chars:,} characters</div>",
                    unsafe_allow_html=True)
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        st.markdown("<div class='sum-btn'>", unsafe_allow_html=True)
        if st.button("✦  SUMMARIZE", key="summarize_btn"):
            if not text_input or len(text_input.strip()) < 50:
                st.warning("⚠️ Please enter at least 50 characters.")
            else:
                with st.spinner("Extracting key sentences…"):
                    try:
                        sm   = extractive_summarize(text_input, num_sentences)
                        stxt = " ".join(sm)
                        sw   = len(stxt.split())
                        red  = round((1 - sw / words) * 100, 1) if words else 0
                        st.session_state.summary        = sm
                        st.session_state.summary_text   = stxt
                        st.session_state.original_words = words
                        st.session_state.last_reduction = red
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Right: Summary ─────────────────────────────────────────────────────────
    with rc:
        st.markdown("""
        <div class="card">
          <div class="card-hdr">
            <div>
              <div class="card-title">Summary</div>
              <div class="card-sub">Extracted key highlights</div>
            </div>
            <div class="dots">···</div>
          </div>
        </div>""", unsafe_allow_html=True)

        if st.session_state.summary:
            sm    = st.session_state.summary
            stxt  = st.session_state.summary_text
            ow    = st.session_state.original_words
            sw    = len(stxt.split())
            red   = st.session_state.last_reduction

            st.markdown(f"""
            <div class="s-title">Key Highlights</div>
            <div class="s-sub">{tone} tone &middot; {len(sm)} sentences &middot; {sw} words</div>
            """, unsafe_allow_html=True)

            bhtml = ""
            for i, s in enumerate(sm, 1):
                ws = s.split()
                disp = f"<strong>{' '.join(ws[:4])}</strong> {' '.join(ws[4:])}" if len(ws) > 4 else s
                bhtml += f'<div class="blt"><span class="blt-n">{i}</span><span>{disp}</span></div>'
            st.markdown(bhtml, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="s-footer">
              Original: {ow:,} words &nbsp;&middot;&nbsp;
              Summary: {sw} words &nbsp;&middot;&nbsp;
              Reduced by <strong>{red}%</strong>
            </div>""", unsafe_allow_html=True)

            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

            # Action buttons
            a1, a2, a3, a4 = st.columns(4)
            with a1:
                st.markdown("<div class='act'>", unsafe_allow_html=True)
                if st.button("📋 Copy", key="btn_copy"):
                    st.toast("Summary text is in the expander below!", icon="📋")
                st.markdown("</div>", unsafe_allow_html=True)
            with a2:
                st.markdown("<div class='act'>", unsafe_allow_html=True)
                if st.button("🔖 Save", key="btn_save"):
                    app_data = load_data()
                    entry = {
                        "id":        len(app_data["library"]) + 1,
                        "title":     " ".join(sm[0].split()[:5]) + "…" if sm else "Summary",
                        "tone":      tone,
                        "length":    length_val,
                        "sentences": len(sm),
                        "words":     sw,
                        "reduction": red,
                        "text":      stxt,
                        "preview":   sm[0][:80] + "…" if sm else "",
                        "date":      datetime.now().strftime("%b %d, %Y %H:%M"),
                        "project":   "",
                    }
                    app_data["library"].insert(0, entry)
                    save_data(app_data)
                    st.toast("🔖 Saved to Library!", icon="✅")
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            with a3:
                st.markdown("<div class='act'>", unsafe_allow_html=True)
                if st.button("↗ Share", key="btn_share"):
                    st.toast("🔗 Share link copied!", icon="✅")
                st.markdown("</div>", unsafe_allow_html=True)
            with a4:
                st.markdown("<div class='act'>", unsafe_allow_html=True)
                st.download_button("⬇ Export", data=stxt,
                    file_name="summary.txt", mime="text/plain", key="btn_export")
                st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("📋 Copy summary text", expanded=False):
                st.text_area("Summary output", value=stxt, height=130,
                             key="copy_area", label_visibility="collapsed")
        else:
            st.markdown("""
            <div class="empty-wrap">
              <div class="empty-ico">✦</div>
              <div class="empty-ttl">Your summary will appear here</div>
              <div class="empty-hint">Paste text on the left and click SUMMARIZE</div>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# LIBRARY
# ════════════════════════════════════════════════════════════════════════════════
elif page == "Library":
    app_data = load_data()
    library  = app_data["library"]

    c1, c2 = st.columns([3, 1])
    with c1:
        search = st.text_input("Search library", placeholder="🔍  Search saved summaries…",
                               label_visibility="collapsed", key="lib_search")
    with c2:
        f_tone = st.selectbox("Filter tone",
            ["All Tones", "Professional", "Casual", "Academic", "Creative"],
            label_visibility="collapsed", key="lib_filter")

    filtered = library
    if search:
        filtered = [x for x in filtered
                    if search.lower() in x.get("text","").lower()
                    or search.lower() in x.get("title","").lower()]
    if f_tone != "All Tones":
        filtered = [x for x in filtered if x.get("tone","") == f_tone]

    st.markdown(f"<div style='font-size:13px;color:#9ca3af;margin-bottom:14px;font-weight:500;'>"
                f"{len(filtered)} item{'s' if len(filtered)!=1 else ''} found</div>",
                unsafe_allow_html=True)

    if not filtered:
        st.markdown("""
        <div class="empty-wrap">
          <div class="empty-ico">📚</div>
          <div class="empty-ttl">No saved summaries yet</div>
          <div class="empty-hint">Generate a summary on Home and click 🔖 Save</div>
        </div>""", unsafe_allow_html=True)
    else:
        for item in filtered:
            with st.expander(f"**{item.get('title','Untitled')}** — {item.get('date','')}"):
                mc = st.columns(4)
                mc[0].metric("Words",     item.get("words","–"))
                mc[1].metric("Sentences", item.get("sentences","–"))
                mc[2].metric("Reduced",   f"{item.get('reduction',0)}%")
                mc[3].metric("Tone",      item.get("tone","–"))

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                bhtml = ""
                for i, s in enumerate(item.get("text","").split(". "), 1):
                    if s.strip():
                        ws   = s.strip().split()
                        disp = f"<strong>{' '.join(ws[:4])}</strong> {' '.join(ws[4:])}" if len(ws) > 4 else s.strip()
                        bhtml += f'<div class="blt"><span class="blt-n">{i}</span><span>{disp}</span></div>'
                st.markdown(bhtml, unsafe_allow_html=True)

                d1, d2, _ = st.columns([1, 1, 3])
                with d1:
                    st.download_button("⬇ Export", data=item.get("text",""),
                        file_name="summary.txt", mime="text/plain", key=f"dl_{item['id']}")
                with d2:
                    if st.button("🗑 Delete", key=f"del_{item['id']}"):
                        app_data["library"] = [x for x in app_data["library"] if x.get("id") != item["id"]]
                        save_data(app_data)
                        st.toast("Deleted", icon="🗑")
                        st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# PROJECTS
# ════════════════════════════════════════════════════════════════════════════════
elif page == "Projects":
    app_data = load_data()
    projects = app_data["projects"]
    library  = app_data["library"]

    with st.expander("➕ Create New Project"):
        pname = st.text_input("Project name", placeholder="e.g. Research Papers, News Articles…",
                              label_visibility="collapsed", key="new_proj_name")
        pdesc = st.text_input("Description (optional)", placeholder="Short description…",
                              label_visibility="collapsed", key="new_proj_desc")
        if st.button("Create Project", key="btn_create_proj"):
            if pname.strip():
                app_data["projects"].append({
                    "id":   len(projects) + 1,
                    "name": pname.strip(),
                    "desc": pdesc.strip(),
                    "date": datetime.now().strftime("%b %d, %Y"),
                })
                save_data(app_data)
                st.toast(f"✅ Project '{pname}' created!", icon="📁")
                st.rerun()
            else:
                st.warning("Please enter a project name.")

    if not projects:
        st.markdown("""
        <div class="empty-wrap">
          <div class="empty-ico">📁</div>
          <div class="empty-ttl">No projects yet</div>
          <div class="empty-hint">Create a project above to group your summaries</div>
        </div>""", unsafe_allow_html=True)
    else:
        for proj in projects:
            proj_items = [x for x in library if x.get("project") == proj["name"]]
            with st.expander(f"**{proj['name']}** — {len(proj_items)} summaries"):
                if proj.get("desc"):
                    st.markdown(f"<div style='font-size:13px;color:#6b7280;margin-bottom:12px;'>{proj['desc']}</div>",
                                unsafe_allow_html=True)

                info_c = st.columns(3)
                info_c[0].metric("Summaries", len(proj_items))
                info_c[1].metric("Created",   proj.get("date","–"))
                info_c[2].metric("ID",        f"#{proj['id']}")

                # Assign unassigned summaries
                unassigned = [x for x in library if not x.get("project")]
                if unassigned:
                    st.markdown("<div style='font-size:13px;font-weight:600;color:#374151;margin:12px 0 6px;'>Add summaries to this project:</div>",
                                unsafe_allow_html=True)
                    for item in unassigned[:5]:
                        rc1, rc2 = st.columns([4, 1])
                        rc1.markdown(f"<div style='font-size:13px;padding:6px 0;color:#374151;'>{item.get('title','Untitled')} <span style='color:#9ca3af;'>({item.get('date','')})</span></div>",
                                     unsafe_allow_html=True)
                        with rc2:
                            if st.button("Add", key=f"add_{item['id']}_p{proj['id']}"):
                                for x in app_data["library"]:
                                    if x.get("id") == item["id"]:
                                        x["project"] = proj["name"]
                                save_data(app_data)
                                st.toast(f"Added to {proj['name']}", icon="✅")
                                st.rerun()

                if proj_items:
                    st.markdown("<div style='font-size:13px;font-weight:600;color:#374151;margin:12px 0 6px;'>Summaries in this project:</div>",
                                unsafe_allow_html=True)
                    for item in proj_items:
                        st.markdown(f"""
                        <div class="lib-card">
                          <div class="lib-title">{item.get('title','Untitled')}</div>
                          <div class="lib-meta">{item.get('date','')} &middot; {item.get('tone','')} &middot; {item.get('words','')} words</div>
                          <div class="lib-preview">{item.get('preview','')}</div>
                        </div>""", unsafe_allow_html=True)

                if st.button("🗑 Delete Project", key=f"del_proj_{proj['id']}"):
                    app_data["projects"] = [p for p in app_data["projects"] if p.get("id") != proj["id"]]
                    for x in app_data["library"]:
                        if x.get("project") == proj["name"]:
                            x["project"] = ""
                    save_data(app_data)
                    st.toast(f"Project '{proj['name']}' deleted", icon="🗑")
                    st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# SETTINGS
# ════════════════════════════════════════════════════════════════════════════════
elif page == "Settings":
    app_data = load_data()
    settings = app_data["settings"]

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("<div class='opt-label' style='margin-bottom:10px;'>Profile</div>", unsafe_allow_html=True)
    new_user = st.text_input("Your display name", value=settings.get("username","User"),
                             placeholder="Enter your name…", key="set_username",
                             label_visibility="visible")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='opt-label' style='margin-bottom:10px;'>Defaults</div>", unsafe_allow_html=True)

    dc1, dc2 = st.columns(2)
    with dc1:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;'>Default Length</div>", unsafe_allow_html=True)
        new_len = st.select_slider("Default length",
            options=["Short","Medium","Long"],
            value=settings.get("default_length","Medium"),
            key="set_length", label_visibility="collapsed")
    with dc2:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;'>Default Tone</div>", unsafe_allow_html=True)
        new_tone = st.selectbox("Default tone",
            ["Professional","Casual","Academic","Creative"],
            index=["Professional","Casual","Academic","Creative"].index(
                settings.get("default_tone","Professional")),
            key="set_tone", label_visibility="collapsed")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='opt-label' style='margin-bottom:10px;'>Data Management</div>", unsafe_allow_html=True)
    dm1, dm2 = st.columns([1, 1])
    with dm1:
        if st.button("🗑 Clear Library", key="btn_clear_lib"):
            app_data["library"] = []
            save_data(app_data)
            st.toast("Library cleared", icon="🗑")
            st.rerun()
    with dm2:
        if st.button("🗑 Clear All Data", key="btn_clear_all"):
            app_data["library"]  = []
            app_data["projects"] = []
            save_data(app_data)
            st.toast("All data cleared", icon="🗑")
            st.rerun()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='save-btn'>", unsafe_allow_html=True)
    if st.button("💾  Save Settings", key="btn_save_settings"):
        app_data["settings"]["username"]       = new_user
        app_data["settings"]["default_length"] = new_len
        app_data["settings"]["default_tone"]   = new_tone
        save_data(app_data)
        st.session_state.current_length = new_len
        st.session_state.current_tone   = new_tone
        st.toast("✅ Settings saved!", icon="💾")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# HELP
# ════════════════════════════════════════════════════════════════════════════════
elif page == "Help":
    HELP_ITEMS = [
        ("✦",  "What is Summarize AI?",
         "Summarize AI uses extractive summarization — it scores every sentence by word frequency and position, then picks the top-N most important ones. Runs entirely on your machine with no API key required."),
        ("📄", "How do I summarize text?",
         "Go to Home, paste your text (or enter a URL), pick a Length and Tone, then click SUMMARIZE. Key sentences appear on the right instantly."),
        ("📚", "What is the Library?",
         "After generating a summary, click 🔖 Save. It's stored in Library. You can search, filter by tone, export as .txt, or delete any entry."),
        ("📁", "What are Projects?",
         "Projects group related summaries. Create a project, then assign Library items to it — great for research, course notes, or news topics."),
        ("⚙️", "Can I change defaults?",
         "Yes — go to Settings to set your name, default summary length, and default tone. These persist across sessions."),
        ("⬇", "How do I export?",
         "Click ⬇ Export on any summary to download a .txt file. You can also select-all in the copy area below the summary."),
        ("🌐", "Does URL fetching always work?",
         "Many sites block automated requests. If a URL fails, copy-paste the text manually. Wikipedia and plain HTML articles work best."),
        ("🔒", "Is my data private?",
         "Yes — all data is saved locally in app_data.json on your computer. Nothing leaves your machine."),
    ]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    for icon, title, desc in HELP_ITEMS:
        st.markdown(f"""
        <div class="help-item">
          <div class="help-icon">{icon}</div>
          <div>
            <div class="help-title">{title}</div>
            <div class="help-desc">{desc}</div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;margin-top:20px;font-size:13px;color:#9ca3af;">
      Built with Python + Streamlit &nbsp;·&nbsp;
      <a href="https://github.com/kdeepak2001/Ai-Text-Summarizer" target="_blank"
         style="color:#4361ee;text-decoration:none;font-weight:600;">View on GitHub ↗</a>
    </div>""", unsafe_allow_html=True)
