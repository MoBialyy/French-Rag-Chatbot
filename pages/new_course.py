import streamlit as st
from utils import nav


def page_new_course():
    st.markdown("""
    <style>
    .page-wrap { padding: 2.5rem; max-width: 600px; margin: 0 auto; }
    .page-back { color: #6060a0; font-size: 0.85rem; cursor: pointer; margin-bottom: 2rem; display: inline-flex; align-items: center; gap: 0.4rem; }
    .page-title { font-size: 1.8rem; font-weight: 700; color: #fff; letter-spacing: -0.02em; margin-bottom: 0.3rem; }
    .page-sub { color: #6060a0; font-size: 0.9rem; margin-bottom: 2rem; }
    .form-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 2rem;
    }
    .icon-grid { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
    .icon-opt {
        width: 48px; height: 48px;
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; cursor: pointer;
        border: 2px solid transparent;
        transition: all 0.15s;
    }
    .icon-opt:hover { background: rgba(108,99,255,0.15); border-color: #6c63ff; }
    .icon-opt.selected { background: rgba(108,99,255,0.2); border-color: #6c63ff; }
    </style>
    <div class="page-wrap">
    """, unsafe_allow_html=True)

    if st.button("← Back to Home"):
        nav("home")

    st.markdown("""
    <div class="page-title">New Course</div>
    <div class="page-sub">Create a new course to start adding lectures</div>
    <div class="form-card">
    """, unsafe_allow_html=True)

    course_name = st.text_input("Course Name", placeholder="e.g. Professional Ethics, NLP, OOP...")

    st.markdown('<div style="margin-top:0.5rem;margin-bottom:0.3rem;color:#9090b8;font-size:0.8rem;font-weight:500;letter-spacing:0.05em;text-transform:uppercase">Pick an Icon</div>', unsafe_allow_html=True)
    icons = ["📚", "⚖️", "🧠", "🔧", "🧪", "💡", "🎯", "🌐", "📊", "🔬", "🖥️", "🎓"]
    selected_icon = st.selectbox("Icon", icons, label_visibility="collapsed")

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Create Course", use_container_width=True, type="primary"):
            if course_name.strip():
                st.session_state.courses[course_name.strip()] = {
                    "icon": selected_icon,
                    "color": "#6c63ff",
                    "lectures": []
                }
                nav("course", current_course=course_name.strip())
            else:
                st.error("Please enter a course name.")
    with col2:
        if st.button("Cancel", use_container_width=True):
            nav("home")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    div[data-testid="column"]:first-child .stButton > button {
        background: linear-gradient(135deg, #6c63ff, #a855f7) !important;
        color: white !important; font-weight: 600 !important;
        box-shadow: 0 4px 20px rgba(108,99,255,0.3) !important;
    }
    div[data-testid="column"]:last-child .stButton > button {
        background: transparent !important; color: #9090b8 !important;
        border: 1px solid #2a2a45 !important;
    }
    </style>
    """, unsafe_allow_html=True)
