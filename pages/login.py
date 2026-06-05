# pages/login.py

import streamlit as st
from utils import nav


def page_login():
    st.markdown("""
    <style>
    [data-testid="stAppViewBlockContainer"] {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 100vh !important;
        padding: 0 !important;
    }

    [data-testid="stVerticalBlock"] > div:has(.login-header) {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(108,99,255,0.2);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        width: 100%;
        max-width: 420px;
        backdrop-filter: blur(20px);
        box-shadow: 0 40px 80px rgba(0,0,0,0.4), 0 0 0 1px rgba(108,99,255,0.1);
    }

    .login-logo {
        font-size: 2.4rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 0.3rem;
        letter-spacing: -0.03em;
        text-align: center;
    }
    .login-logo span { color: #6c63ff; }

    .login-tagline {
        color: #6060a0;
        font-size: 0.85rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
        text-align: center;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6c63ff, #a855f7) !important;
        color: white !important;
        font-weight: 600 !important;
        width: 100%;
        border: none !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 4px 20px rgba(108,99,255,0.3) !important;
    }

    div.stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #9090b8 !important;
        border: 1px solid #2a2a45 !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-header"></div>', unsafe_allow_html=True)
        st.markdown('<div class="login-logo">Paul le <span>Tuteur</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="login-tagline">Votre tuteur universitaire intelligent</div>', unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="your username")
        password = st.text_input("Password", placeholder="••••••••", type="password")

        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

        if st.button("Sign In", use_container_width=True, type="primary"):
            if username and password:
                st.session_state.user = username
                nav("home")
            else:
                st.error("Please fill in all fields.")

        if st.button("Sign Up", use_container_width=True, type="secondary"):
            st.info("Sign up coming soon!")
