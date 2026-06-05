# pages/chat.py

import streamlit as st
from utils import nav, to_collection_name
from config import RETRIEVAL_TOP_K
from clients.rag_client import retrieve
from clients.mistral_client import chat_stream, translate_to_english


def page_chat():
    course_name = st.session_state.current_course
    chat_mode   = st.session_state.chat_mode
    lecture     = st.session_state.current_lecture

    if chat_mode == "lecture" and lecture:
        context_label = f"Lecture {lecture['num']} — {lecture['title']}"
        context_sub   = course_name
        lecture_num   = lecture["num"]
    else:
        context_label = course_name
        context_sub   = "All lectures"
        lecture_num   = None

    # ── Header ─────────────────────────────────────────────────────────────
    badge_color = "rgba(108,99,255,0.2)" if chat_mode == "course" else "rgba(67,233,123,0.15)"
    badge_text  = "rgba(160,144,255,1)"  if chat_mode == "course" else "rgba(67,233,123,1)"
    badge_label = "Course" if chat_mode == "course" else "Lecture"

    st.markdown(f"""
        <style>
        .chat-header {{
            padding: 1.2rem 2rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            display: flex; align-items: center; gap: 1rem;
            background: rgba(255,255,255,0.02);
        }}
        .chat-context-label {{ font-size: 1rem; font-weight: 600; color: #fff; }}
        .chat-context-sub   {{ font-size: 0.75rem; color: #6060a0; margin-top: 0.1rem; }}
        .chat-badge {{
            padding: 0.2rem 0.6rem; border-radius: 20px;
            font-size: 0.7rem; font-weight: 600;
            background: {badge_color}; color: {badge_text};
            text-transform: uppercase; letter-spacing: 0.05em;
        }}

        /* Style native chat messages */
        [data-testid="stChatMessage"] {{
            background: rgba(255,255,255,0.02) !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
            border-radius: 12px !important;
            margin-bottom: 0.5rem !important;
        }}
        [data-testid="stChatInputTextArea"] {{
            background: #13131f !important;
            border: 1px solid #2a2a45 !important;
            color: #e8e8f0 !important;
            font-family: 'Sora', sans-serif !important;
        }}
        </style>

        <div class="chat-header">
            <div style="flex:1">
                <div style="display:flex;align-items:center;gap:0.6rem">
                    <div class="chat-context-label">{context_label}</div>
                    <div class="chat-badge">{badge_label}</div>
                </div>
                <div class="chat-context-sub">{context_sub}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    if st.button("← Back to Course"):
        nav("course")

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    # ── Message history ────────────────────────────────────────────────────
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ── Chat input ─────────────────────────────────────────────────────────
    if prompt := st.chat_input("Posez votre question ici..."):

        # Show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Skip retrieval for short/casual messages
        if len(prompt.strip()) > 15:
            english_query = translate_to_english(prompt)
            chunks = []
            try:
                chunks = retrieve(
                    query=english_query,
                    collection=to_collection_name(course_name),
                    top_k=RETRIEVAL_TOP_K,
                    lecture_num=lecture_num,
                )
                print(f"\n=== RETRIEVED CHUNKS ===")
                for c in chunks:
                    print(f"  [{c.get('fused_score', 0):.2f}] {c['chunk_id']} — {c['text'][:80]}")
                print(f"========================\n")
            except Exception:
                pass
        else:
            chunks = []

        # Stream response from Mistral
        with st.chat_message("assistant"):
            placeholder   = st.empty()
            full_response = ""
            cursor        = "▌"
            try:
                # Keep only last 10 messages to avoid context overflow
                history_window = st.session_state.messages[-10:]
                for token in chat_stream(
                    messages=history_window,
                    context_chunks=chunks,
                ):
                    full_response += token
                    placeholder.markdown(full_response + cursor)
                placeholder.markdown(full_response)
            except Exception as e:
                full_response = f"⚠️ Erreur: {str(e)}"
                placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})