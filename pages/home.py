import streamlit as st
from utils import nav


def page_home():
    st.markdown("""
    <style>
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.4rem 2.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        background: rgba(255,255,255,0.02);
        backdrop-filter: blur(10px);
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .topbar-logo { font-size: 1.4rem; font-weight: 700; color: #fff; letter-spacing: -0.03em; }
    .topbar-logo span { color: #6c63ff; }
    .topbar-user {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        color: #9090b8;
        font-size: 0.85rem;
    }
    .avatar {
        width: 32px; height: 32px;
        background: linear-gradient(135deg, #6c63ff, #a855f7);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        color: white; font-weight: 600; font-size: 0.8rem;
    }
    .home-content { padding: 2.5rem; }
    .home-header { margin-bottom: 2rem; }
    .home-greeting {
        font-size: 1.8rem; font-weight: 700;
        color: #fff; letter-spacing: -0.02em;
        margin-bottom: 0.3rem;
    }
    .home-sub { color: #6060a0; font-size: 0.9rem; }
    .section-title {
        font-size: 0.75rem; font-weight: 600;
        color: #6060a0; letter-spacing: 0.1em;
        text-transform: uppercase; margin-bottom: 1rem;
    }
    .course-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.2s ease;
        cursor: pointer;
        height: 100%;
    }
    .course-card:hover {
        background: rgba(108,99,255,0.08);
        border-color: rgba(108,99,255,0.3);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }
    .course-icon {
        font-size: 2rem; margin-bottom: 1rem;
        width: 52px; height: 52px;
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
    }
    .course-name {
        font-size: 1.1rem; font-weight: 600;
        color: #fff; margin-bottom: 0.3rem;
    }
    .course-meta { color: #6060a0; font-size: 0.8rem; }
    .course-bar {
        height: 3px; border-radius: 2px;
        margin-top: 1.2rem;
        background: rgba(255,255,255,0.05);
        overflow: hidden;
    }
    .course-bar-fill {
        height: 100%; border-radius: 2px;
        background: linear-gradient(90deg, #6c63ff, #a855f7);
        width: 60%;
    }
    </style>
    """, unsafe_allow_html=True)

    user_initial = st.session_state.user[0].upper() if st.session_state.user else "U"

    # Topbar
    col_logo, col_user = st.columns([6, 1])
    with col_logo:
        st.markdown(f"""
        <div class="topbar-logo" style="padding:1.4rem 0 1rem 0">
            Paul le <span>Tuteur</span>
        </div>
        """, unsafe_allow_html=True)
    with col_user:
        st.markdown(f"""
        <div class="topbar-user" style="padding-top:1.2rem;justify-content:flex-end">
            <div class="avatar">{user_initial}</div>
            <span>{st.session_state.user}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,0.05);margin:0 0 2rem 0">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="home-header">
        <div class="home-greeting">Bonjour, {st.session_state.user} 👋</div>
        <div class="home-sub">Que souhaitez-vous apprendre aujourd'hui ?</div>
    </div>
    """, unsafe_allow_html=True)

    # Actions row
    col_title, col_btn = st.columns([5, 1])
    with col_title:
        st.markdown('<div class="section-title">Mes cours</div>', unsafe_allow_html=True)
    with col_btn:
        if st.button("＋ New Course", use_container_width=True):
            nav("new_course")

    st.markdown("""
    <style>
    div[data-testid="column"]:last-child .stButton > button {
        background: linear-gradient(135deg, #6c63ff, #a855f7) !important;
        color: white !important; font-weight: 600 !important;
        font-size: 0.8rem !important;
        box-shadow: 0 4px 20px rgba(108,99,255,0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Course grid
    courses = st.session_state.courses
    if not courses:
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;color:#3d3d6b">
            <div style="font-size:3rem;margin-bottom:1rem">📚</div>
            <div style="font-size:1rem">No courses yet. Create your first one!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for i, (name, data) in enumerate(courses.items()):
            with cols[i % 3]:
                lec_count = len(data["lectures"])
                if st.button(f"{data['icon']}  {name}\n{lec_count} lecture{'s' if lec_count != 1 else ''}", key=f"open_{name}", use_container_width=True):
                    nav("course", current_course=name)

    st.markdown("""
        <style>
        .stButton > button {
            background: rgba(255,255,255,0.03) !important;
            color: #fff !important;
            border: 1px solid rgba(255,255,255,0.07) !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            text-align: left !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            height: auto !important;
            min-height: 90px !important;
            white-space: pre-wrap !important;
            line-height: 1.6 !important;
        }
        .stButton > button:hover {
            background: rgba(108,99,255,0.08) !important;
            border-color: rgba(108,99,255,0.3) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(0,0,0,0.3) !important;
        }
        </style>
        """, unsafe_allow_html=True)
