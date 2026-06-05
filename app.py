# app.py
"""
Entry point — page config, global CSS, and router only.
All page logic lives in pages/.
"""

import streamlit as st
from utils import init_state

from pages.login       import page_login
from pages.home        import page_home
from pages.new_course  import page_new_course
from pages.course      import page_course
from pages.add_lecture import page_add_lecture
from pages.chat        import page_chat
from pages.study       import page_study

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Paul le Tuteur",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e8f0 !important;
    font-family: 'Sora', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #1a1035 0%, #0a0a0f 50%, #0d1a2e 100%) !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarNav"],
[data-testid="stSidebar"] { display: none !important; }

.main .block-container { padding: 0 !important; max-width: 100% !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #3d3d6b; border-radius: 2px; }

.stButton > button {
    font-family: 'Sora', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover  { transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0px) !important; }

.stTextInput > div > div > input,
.stTextArea  > div > div > textarea {
    font-family: 'Sora', sans-serif !important;
    background:  #13131f !important;
    border: 1px solid #2a2a45 !important;
    color: #e8e8f0 !important;
    border-radius: 10px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea  > div > div > textarea:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.15) !important;
}
.stTextInput label, .stTextArea label {
    font-family: 'Sora', sans-serif !important;
    color: #9090b8 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}
</style>
""", unsafe_allow_html=True)

# ── Init + route ───────────────────────────────────────────────────────────
init_state()

page = st.session_state.page

if page == "login":
    page_login()
elif page == "home":
    if not st.session_state.user:
        st.session_state.page = "login"
        st.rerun()
    page_home()
elif page == "new_course":
    page_new_course()
elif page == "course":
    page_course()
elif page == "add_lecture":
    page_add_lecture()
elif page == "chat":
    page_chat()
elif page == "study":
    page_study()
