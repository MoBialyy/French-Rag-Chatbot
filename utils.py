# utils.py
"""
Shared utilities used across all pages.
"""

import streamlit as st


def nav(page: str, **kwargs):
    """Navigate to a page and optionally set session state values."""
    st.session_state.page = page
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.rerun()


def init_state():
    """Initialize all session state keys with defaults on first load."""
    defaults = {
        "page":               "login",
        "user":               None,
        "current_course":     None,
        "current_lecture":    None,
        "chat_mode":          None,   # "course" or "lecture"
        "messages":           [],
        "study_chunk_index":  0,
        "courses":            {},     # { course_name: { icon, color, lectures: [] } }
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def to_collection_name(course_name: str) -> str:
    """Convert course name to a ChromaDB-safe collection name."""
    import re
    name = course_name.lower().strip()
    name = re.sub(r'[^a-z0-9]+', '_', name)  # replace invalid chars with _
    name = name.strip('_')                     # remove leading/trailing underscores
    return name or "collection"
