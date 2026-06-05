# pages/study.py
 
import streamlit as st
from utils import nav, to_collection_name
from clients.rag_client import get_chunk
from clients.mistral_client import chat_stream
import re
 
 
EXPLAIN_PROMPT = (
    "En tant que tuteur universitaire, explique ce contenu de cours "
    "en français de façon claire et pédagogique, avec des exemples si nécessaire. "
    "Ne mentionne jamais les numéros de slides. "
    "Le contenu peut être en anglais ou en arabe, mais réponds toujours en français.\n\n"
    "IMPORTANT: Ta réponse doit être entièrement en français.\n\n"
    "{chunk_text}"
)

def _clean_chunk(text: str) -> str:
    """Remove slide headers and clean up the text before sending to Mistral."""
    text = re.sub(r'##\s*Slide\s*\d+[^\n]*\n', '', text)  # remove ## Slide X lines
    text = re.sub(r'\n{3,}', '\n\n', text)                 # collapse extra newlines
    return text.strip()


def _get_explanation(chunk_text: str) -> str:
    """Ask Mistral to explain the chunk. Returns full response as string."""
    clean_text = _clean_chunk(chunk_text)
    messages = [
        {
            "role": "user",
            "content": EXPLAIN_PROMPT.format(chunk_text=clean_text)
        }
    ]
    full_response = ""
    for token in chat_stream(messages=messages, context_chunks=[]):
        full_response += token
    return full_response
 
 
def page_study():
    course_name   = st.session_state.current_course
    lecture       = st.session_state.current_lecture
    chunk_index   = st.session_state.study_chunk_index
 
    if not lecture:
        st.error("No lecture selected.")
        if st.button("← Back"):
            nav("course")
        return
 
    lecture_num   = lecture["num"]
    lecture_title = lecture["title"]
 
    # ── Header ─────────────────────────────────────────────────────────────
    st.markdown(f"""
    <style>
    .study-header {{
        padding: 1.5rem 2.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        background: rgba(255,255,255,0.02);
    }}
    .study-title {{ font-size: 1.4rem; font-weight: 700; color: #fff; }}
    .study-sub   {{ font-size: 0.8rem; color: #6060a0; margin-top: 0.2rem; }}
    .study-card {{
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1.5rem;
        line-height: 1.8;
        color: #d0d0e8;
        font-size: 0.92rem;
    }}
    .study-progress {{
        font-size: 0.75rem; font-weight: 600;
        color: #6060a0; letter-spacing: 0.08em;
        text-transform: uppercase; margin-bottom: 1rem;
    }}
    </style>
 
    <div class="study-header">
        <div class="study-title">📖 {lecture_title}</div>
        <div class="study-sub">{course_name} · Lecture {lecture_num}</div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown('<div style="padding: 1.5rem 2.5rem;">', unsafe_allow_html=True)
 
    if st.button("← Back to Course"):
        nav("course")
 
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
 
    # ── Load chunk ─────────────────────────────────────────────────────────
    try:
        chunk_data = get_chunk(
            collection=to_collection_name(course_name),
            lecture_num=lecture_num,
            chunk_index=chunk_index,
        )
    except Exception as e:
        st.error(f"Could not load chunk: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
        return
 
    total_chunks = chunk_data["total_chunks"]
    is_last      = chunk_data["is_last"]
    chunk_text   = chunk_data["text"]
 
    # ── Progress bar ───────────────────────────────────────────────────────
    progress = (chunk_index + 1) / total_chunks
    st.markdown(
        f'<div class="study-progress">Section {chunk_index + 1} of {total_chunks}</div>',
        unsafe_allow_html=True
    )
    st.progress(progress)
 
    # ── Get explanation from Mistral ───────────────────────────────────────
    cache_key = f"study_explanation_{course_name}_{lecture_num}_{chunk_index}"
 
    if cache_key not in st.session_state:
        with st.spinner("Paul prépare l'explication..."):
            try:
                explanation = _get_explanation(chunk_text)
                st.session_state[cache_key] = explanation
            except Exception as e:
                st.session_state[cache_key] = f"⚠️ Erreur lors de la génération: {str(e)}"
 
    explanation = st.session_state[cache_key]
 
    # ── Display explanation ────────────────────────────────────────────────
    st.markdown(f'<div class="study-card">{explanation}</div>', unsafe_allow_html=True)
 
    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
 
    # ── Navigation buttons ─────────────────────────────────────────────────
    col_prev, col_next = st.columns([1, 1])
 
    with col_prev:
        prev_disabled = chunk_index == 0
        if st.button(
            "← Previous",
            use_container_width=True,
            disabled=prev_disabled,
            key="study_prev"
        ):
            st.session_state.study_chunk_index -= 1
            st.rerun()
 
    with col_next:
        if is_last:
            if st.button("✅ Finish", use_container_width=True, key="study_finish"):
                nav("course")
        else:
            if st.button("Next →", use_container_width=True, key="study_next"):
                st.session_state.study_chunk_index += 1
                st.rerun()
 
    st.markdown("""
    <style>
    div[data-testid="column"]:last-child .stButton > button {
        background: linear-gradient(135deg, #6c63ff, #a855f7) !important;
        color: white !important; font-weight: 600 !important;
        box-shadow: 0 4px 20px rgba(108,99,255,0.3) !important;
    }
    div[data-testid="column"]:first-child .stButton > button {
        background: transparent !important;
        color: #9090b8 !important;
        border: 1px solid #2a2a45 !important;
    }
    </style>
    """, unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)