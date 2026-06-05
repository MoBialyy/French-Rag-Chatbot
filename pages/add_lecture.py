# pages/add_lecture.py

import os
import time
import streamlit as st

from utils import nav, to_collection_name
from config import UPLOADS_DIR
from clients.rag_client import ingest_lecture, get_job_status


def _save_upload(uploaded_file) -> str:
    """Save Streamlit UploadedFile to disk, return absolute path."""
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return os.path.abspath(file_path)


def page_add_lecture():
    course_name = st.session_state.current_course
    course      = st.session_state.courses.get(course_name, {})
    lectures    = course.get("lectures", [])
    next_num    = max([l["num"] for l in lectures], default=0) + 1

    st.markdown("""
    <style>
    .page-wrap { padding: 2.5rem; max-width: 600px; margin: 0 auto; }
    .form-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1rem;
    }
    </style>
    <div class="page-wrap">
    """, unsafe_allow_html=True)

    if st.button("← Back to Course"):
        nav("course")

    st.markdown(f"""
    <div style="margin-top:1.5rem">
        <div style="font-size:1.8rem;font-weight:700;color:#fff;letter-spacing:-0.02em">Add Lecture</div>
        <div style="color:#6060a0;font-size:0.9rem;margin-top:0.3rem">
            Adding to: <span style="color:#9090c8">{course_name}</span>
        </div>
    </div>
    <div class="form-card">
    """, unsafe_allow_html=True)

    col_num, col_title = st.columns([1, 2])
    with col_num:
        lec_num = st.number_input("Lecture #", min_value=1, value=next_num, step=1)
    with col_title:
        lec_title = st.text_input("Lecture Title", placeholder="e.g. Introduction to Ethics")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    replace       = st.checkbox("Replace if lecture number already exists", value=True)

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

    col_save, col_cancel = st.columns([1, 1])
    with col_save:
        if st.button("Add Lecture", use_container_width=True, type="primary"):
            if not lec_title.strip():
                st.error("Please enter a lecture title.")
            elif not uploaded_file:
                st.error("Please upload a PDF file.")
            else:
                # 1. Save file to disk
                try:
                    file_path = _save_upload(uploaded_file)
                except Exception as e:
                    st.error(f"Failed to save file: {e}")
                    st.stop()

                # 2. Send to RAG API — retry until server is up
                job = None
                with st.status("Connecting to RAG server...", expanded=False) as rag_status:
                    while True:
                        try:
                            job = ingest_lecture(
                                file_path=file_path,
                                collection=to_collection_name(course_name),
                                lecture_num=int(lec_num),
                                lecture_title=lec_title.strip(),
                                replace=replace,
                            )
                            rag_status.update(label="Connected!", state="complete")
                            break
                        except Exception:
                            rag_status.update(label="Waiting for RAG server...")
                            time.sleep(1)

                # 3. Poll until done
                with st.status("Processing lecture...", expanded=True) as status:
                    job_id = job["job_id"]
                    while True:
                        try:
                            result = get_job_status(job_id)
                        except Exception as e:
                            status.update(label=f"Polling error: {e}", state="error")
                            st.stop()

                        if result["status"] == "done":
                            status.update(label="Lecture processed successfully!", state="complete")
                            break
                        elif result["status"] == "failed":
                            status.update(
                                label=f"Processing failed: {result.get('message', '')}",
                                state="error"
                            )
                            st.stop()
                        else:
                            status.update(label=f"Processing... ({result['status']})")
                            time.sleep(2)

                # 4. Update session state
                lectures_list = st.session_state.courses[course_name]["lectures"]
                existing = next((i for i, l in enumerate(lectures_list) if l["num"] == int(lec_num)), None)

                if existing is not None and replace:
                    lectures_list[existing] = {
                        "num":   int(lec_num),
                        "title": lec_title.strip(),
                        "file":  uploaded_file.name,
                    }
                elif existing is None:
                    lectures_list.append({
                        "num":   int(lec_num),
                        "title": lec_title.strip(),
                        "file":  uploaded_file.name,
                    })
                    lectures_list.sort(key=lambda x: x["num"])

                nav("course")

    with col_cancel:
        if st.button("Cancel", use_container_width=True):
            nav("course")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    div[data-testid="column"]:first-child .stButton > button {
        background: linear-gradient(135deg, #6c63ff, #a855f7) !important;
        color: white !important; font-weight: 600 !important;
        box-shadow: 0 4px 20px rgba(108,99,255,0.3) !important;
    }
    div[data-testid="column"]:last-child .stButton > button {
        background: transparent !important;
        color: #9090b8 !important;
        border: 1px solid #2a2a45 !important;
    }
    </style>
    """, unsafe_allow_html=True)
