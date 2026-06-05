# pages/course.py

import streamlit as st
from utils import nav


def page_course():
    course_name = st.session_state.current_course
    course      = st.session_state.courses.get(course_name, {})
    lectures    = course.get("lectures", [])
    color       = course.get("color", "#6c63ff")
    icon        = course.get("icon", "📚")

    st.markdown(f"""
    <style>
    .course-hero {{
        padding: 2.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        background: linear-gradient(135deg, {color}11 0%, transparent 60%);
    }}
    .course-hero-top {{ display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; }}
    .course-hero-icon {{
        width: 64px; height: 64px;
        background: {color}22;
        border: 1px solid {color}44;
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        font-size: 2rem;
    }}
    .course-hero-name {{ font-size: 2rem; font-weight: 700; color: #fff; letter-spacing: -0.02em; }}
    .course-hero-meta {{ color: #6060a0; font-size: 0.85rem; margin-top: 0.2rem; }}
    .lectures-section {{ padding: 2rem 2.5rem; }}
    .section-title {{
        font-size: 0.75rem; font-weight: 600;
        color: #6060a0; letter-spacing: 0.1em;
        text-transform: uppercase; margin-bottom: 1rem;
    }}
    .lec-row {{
        display: flex; align-items: center;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
        gap: 1rem;
    }}
    .lec-num {{
        width: 32px; height: 32px; min-width: 32px;
        background: {color}22; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.75rem; font-weight: 600; color: {color};
        font-family: 'JetBrains Mono', monospace;
    }}
    .lec-title {{ flex: 1; font-size: 0.9rem; color: #c0c0e0; font-weight: 500; }}
    .empty-lecs {{
        text-align: center; padding: 3rem;
        color: #3d3d6b; font-size: 0.9rem;
    }}
    </style>

    <div class="course-hero">
        <div class="course-hero-top">
            <div class="course-hero-icon">{icon}</div>
            <div>
                <div class="course-hero-name">{course_name}</div>
                <div class="course-hero-meta">{len(lectures)} lecture{"s" if len(lectures) != 1 else ""}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Top action bar ─────────────────────────────────────────────────────
    st.markdown('<div style="padding: 1.5rem 2.5rem 0">', unsafe_allow_html=True)
    col_back, col_chat, col_add = st.columns([2, 2, 2])
    with col_back:
        if st.button("← Home", use_container_width=True):
            nav("home")
    with col_chat:
        if st.button(f"💬 Chat — {course_name}", use_container_width=True):
            st.session_state.messages = []
            nav("chat", chat_mode="course")
    with col_add:
        if st.button("＋ Add Lecture", use_container_width=True):
            nav("add_lecture")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <style>
    .stButton > button {
        background: rgba(255,255,255,0.04) !important;
        color: #9090b8 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }
    .stButton > button:hover {
        border-color: #6c63ff !important;
        color: #fff !important;
        background: rgba(108,99,255,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Lectures list ──────────────────────────────────────────────────────
    st.markdown('<div class="lectures-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Lectures</div>', unsafe_allow_html=True)

    if not lectures:
        st.markdown(
            '<div class="empty-lecs">📄 No lectures yet — add your first one above</div>',
            unsafe_allow_html=True
        )
    else:
        for lec in lectures:
            col_info, col_chat_btn, col_study_btn = st.columns([5, 1, 1])

            with col_info:
                st.markdown(f"""
                <div class="lec-row">
                    <div class="lec-num">{lec['num']:02d}</div>
                    <div class="lec-title">{lec['title']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_chat_btn:
                st.markdown('<div style="padding-top:0.3rem"></div>', unsafe_allow_html=True)
                if st.button("💬 Chat", key=f"chat_{lec['num']}", use_container_width=True):
                    st.session_state.messages = []
                    nav("chat", chat_mode="lecture", current_lecture=lec)

            with col_study_btn:
                st.markdown('<div style="padding-top:0.3rem"></div>', unsafe_allow_html=True)
                # Build the PDF filename from lecture num + title (must match how it was uploaded)
                st.markdown(
                    f'<a href="/app/static/{lec["file"]}" target="_blank" style="text-decoration:none">'
                    f'<button style="width:100%;padding:0.4rem;background:rgba(255,255,255,0.04);'
                    f'color:#9090b8;border:1px solid rgba(255,255,255,0.08);border-radius:10px;'
                    f'cursor:pointer;font-family:Sora,sans-serif;font-size:0.85rem">📖 Study</button>'
                    f'</a>',
                    unsafe_allow_html=True
                )

    st.markdown('</div>', unsafe_allow_html=True)
