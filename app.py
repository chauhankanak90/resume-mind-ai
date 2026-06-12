import streamlit as st
import base64
import os
from llm import generate_resume_data
from pdf_generator import compile_pdf

# 1. Page Config
st.set_page_config(page_title="ResumeMind // AI Optimizer", page_icon="🎯", layout="wide")

# 2. Authentication Logic
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<h1 style='text-align: center;'>🔐 ResumeMind AI - Secure Access</h1>", unsafe_allow_html=True)
        password = st.text_input("Enter Access Password", type="password")
        if st.button("Submit"):
            # Check password against Streamlit Secrets
            if password == st.secrets["APP_PASSWORD"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Incorrect Password")
        return False
    return True

# 3. App Execution (Only runs if authenticated)
if check_password():
    # Inject Custom Premium Dark UI Layout Architecture Style Sheet
    st.markdown("""
        <style>
        .stApp { background-color: #0B0F19; }
        h1, h2, h3, p, label, .stTabs button { font-family: 'Inter', 'Segoe UI', sans-serif !important; }
        .main-title { font-size: 44px !important; font-weight: 800 !important; letter-spacing: -1.5px !important; background: linear-gradient(90deg, #FFFFFF 0%, #A0AEC0 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px; }
        .main-subtitle { color: #64748B !important; font-size: 14px !important; margin-top: -5px; margin-bottom: 35px; }
        .premium-card { background: rgba(17, 24, 39, 0.7); border: 1px solid rgba(255, 255, 255, 0.05); padding: 24px; border-radius: 12px; margin-bottom: 20px; }
        .pipeline-step { background: rgba(30, 41, 59, 0.4); border-left: 4px solid #475569; padding: 12px 16px; border-radius: 0px 8px 8px 0px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }
        .pipeline-step.active { border-left-color: #FF5A1F; background: rgba(255, 90, 31, 0.05); }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">ResumeMind</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">An elegant local AI optimization pipeline engineered to build ATS-hardened resumes.</p>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        st.markdown('<p style="color: #FF5A1F; font-weight: 700; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">Workspace Input Module</p>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            tab_personal, tab_exp, tab_projects, tab_edu, tab_skills, tab_cert, tab_jd = st.tabs([
                "👤 Profile", "💼 Experience", "🚀 Projects", "🎓 Education", "🛠️ Skills", "📜 Certificates", "🎯 Target JD"
            ])
            with tab_personal:
                name_input = st.text_input("Full Name", placeholder="Rahul Sharma")
                contact_input = st.text_input("Contact Details", placeholder="rahul@email.com | +91 98765 43210")
            with tab_exp: exp_input = st.text_area("Responsibilities:", height=180)
            with tab_projects: projects_input = st.text_area("Technical Projects:", height=180)
            with tab_edu: edu_input = st.text_area("Education:", height=120)
            with tab_skills: skills_input = st.text_area("Skills:", height=120)
            with tab_cert: cert_input = st.text_area("Certifications:", height=120)
            with tab_jd: jd_input = st.text_area("Target JD:", height=180)
            st.markdown('</div>', unsafe_allow_html=True)
        generate_btn = st.button("⚡ Run Optimization Pipeline", use_container_width=True, type="primary")

    with col_right:
        st.markdown('<p style="color: #64748B; font-weight: 700; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">Pipeline Status</p>', unsafe_allow_html=True)
        with st.sidebar:
            selected_model = st.selectbox("LLM Base Engine:", ["llama3", "gemma2:2b", "qwen2.5:3b"])
            selected_layout = st.selectbox("Layout:", ["Elite Minimalist"])

        with st.container():
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            s1_active = "active" if generate_btn else ""
            st.markdown(f'''
                <div class="pipeline-step {s1_active}">
                    <div><span style="color: #FF5A1F; font-weight: bold; margin-right: 8px;">01</span>Contextual Analysis</div>
                    <span style="color: #64748B; font-size: 11px;">{"PROCESSING" if generate_btn else "WAITING"}</span>
                </div>
            ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if generate_btn:
            with st.spinner("Processing local AI calculations..."):
                structured_json = generate_resume_data(name_input, contact_input, exp_input, projects_input, edu_input, skills_input, cert_input, jd_input, selected_model)
                if structured_json:
                    pdf_file_path = compile_pdf(structured_json, template_style=selected_layout)
                    if os.path.exists(pdf_file_path):
                        st.success("🎉 Compiled successfully!")
                        with open(pdf_file_path, "rb") as f:
                            st.download_button("📥 Download PDF", f, file_name="Resume.pdf", mime="application/pdf", use_container_width=True)