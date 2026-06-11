# app.py

import streamlit as st
import base64
import os
from llm import generate_resume_data
from pdf_generator import compile_pdf

# Set layout config to wide mode for dashboard split structure
st.set_page_config(page_title="ResumeMind // AI Optimizer", page_icon="🎯", layout="wide")

# Inject Custom Premium Dark UI Layout Architecture Style Sheet
st.markdown("""
    <style>
    /* Background Canvas */
    .stApp { background-color: #0B0F19; }
    
    /* Global Typography Reset */
    h1, h2, h3, p, label, .stTabs button {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    /* Branding Header Typography */
    .main-title {
        font-size: 44px !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
        background: linear-gradient(90deg, #FFFFFF 0%, #A0AEC0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .main-subtitle {
        color: #64748B !important;
        font-size: 14px !important;
        margin-top: -5px;
        margin-bottom: 35px;
    }
    
    /* Translucent Panels */
    .premium-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* Live Pipeline Status Element Rows */
    .pipeline-step {
        background: rgba(30, 41, 59, 0.4);
        border-left: 4px solid #475569;
        padding: 12px 16px;
        border-radius: 0px 8px 8px 0px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .pipeline-step.active {
        border-left-color: #FF5A1F;
        background: rgba(255, 90, 31, 0.05);
    }
    
    /* Input Form Field Skin Updates */
    div.stTextInput > div > div > input, div.stTextArea > div > div > textarea, div.stSelectbox > div > div > div {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# App Branding Header Layout
st.markdown('<h1 class="main-title">ResumeMind</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">An elegant local AI optimization pipeline engineered to build ATS-hardened resumes.</p>', unsafe_allow_html=True)

# Split Layout Configuration
col_left, col_right = st.columns([1.1, 0.9], gap="large")

with col_left:
    st.markdown('<p style="color: #FF5A1F; font-weight: 700; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">Workspace Input Module</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        
        # Modular Workspace Input Tab Rows (Includes Projects and Certificates)
        tab_personal, tab_exp, tab_projects, tab_edu, tab_skills, tab_cert, tab_jd = st.tabs([
            "👤 Profile", "💼 Experience", "🚀 Projects", "🎓 Education", "🛠️ Skills", "📜 Certificates", "🎯 Target JD"
        ])
        
        with tab_personal:
            name_input = st.text_input("Full Name", placeholder="Rahul Sharma")
            contact_input = st.text_input("Contact Details", placeholder="rahul@email.com | +91 98765 43210 | New Delhi")
            
        with tab_exp:
            exp_input = st.text_area("Responsibilities & Accomplishments:", placeholder="Describe professional roles...", height=180)
            
        with tab_projects:
            projects_input = st.text_area("Technical Projects text:", placeholder="WhatsApp HR Bot (Node.js) - Built a scalable data pipeline...", height=180)
            
        with tab_edu:
            edu_input = st.text_area("Academic Credentials:", placeholder="B.Tech in Computer Science...", height=120)
            
        with tab_skills:
            skills_input = st.text_area("Core Capabilities (separated by commas):", placeholder="Power BI, Python, SQL, Git", height=120)
            
        with tab_cert:
            cert_input = st.text_area("Certifications & Licensing:", placeholder="Nodejs - The Complete Guide (Udemy, 2025)", height=120)
            
        with tab_jd:
            jd_input = st.text_area("Target Job Description Context:", placeholder="Paste target job specifications here to map deficits...", height=180)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    generate_btn = st.button("⚡ Run Optimization Pipeline", use_container_width=True, type="primary")

with col_right:
    st.markdown('<p style="color: #64748B; font-weight: 700; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">Pipeline Status & Canvas Render</p>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<h3 style="color: #FFFFFF; font-size: 18px; font-weight: 700; margin-bottom: 20px;">Configuration</h3>', unsafe_allow_html=True)
        selected_model = st.selectbox("LLM Base Engine:", ["llama3", "gemma2:2b", "qwen2.5:3b"], index=0)
        selected_layout = st.selectbox("Document Layout Style Template:", ["Elite Minimalist"], index=0)

    # Replicated ResearchMind Status Panel
    with st.container():
        st.markdown('<div class="premium-card" style="padding: 16px; margin-bottom: 20px;">', unsafe_allow_html=True)
        s1_active = "active" if generate_btn else ""
        st.markdown(f'''
            <div class="pipeline-step {s1_active}">
                <div>
                    <span style="color: #FF5A1F; font-weight: bold; margin-right: 8px;">01</span>
                    <span style="color: #FFFFFF; font-size: 13px; font-weight: 500;">Contextual Analysis Engine</span>
                </div>
                <span style="color: #64748B; font-size: 11px;">{"PROCESSING" if generate_btn else "WAITING"}</span>
            </div>
            <div class="pipeline-step {'active' if generate_btn else ''}">
                <div>
                    <span style="color: #FF5A1F; font-weight: bold; margin-right: 8px;">02</span>
                    <span style="color: #FFFFFF; font-size: 13px; font-weight: 500;">ReportLab Document Compilation Matrix</span>
                </div>
                <span style="color: #64748B; font-size: 11px;">{"COMPILING" if generate_btn else "WAITING"}</span>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Active Execution Pipeline
    if generate_btn:
        if not name_input or not exp_input:
            st.error("Name and Experience validation parameters are required.")
        else:
            with st.spinner("Processing local AI calculations..."):
                # Call updated multi-variable generator
                structured_json = generate_resume_data(
                    name_input, contact_input, exp_input, projects_input, edu_input, skills_input, cert_input, jd_input, selected_model
                )
                
                if structured_json:
                    if jd_input.strip():
                        score = structured_json.get("ats_score", 50)
                        st.metric(label="Calculated ATS Structural Match Alignment Score", value=f"{score}%")
                        missing_kw = structured_json.get("missing_keywords", [])
                        if missing_kw:
                            st.info(f"💡 **Recommended Additions:** {', '.join(missing_kw)}")
                    
                    pdf_file_path = compile_pdf(structured_json, template_style=selected_layout)
                    
                    if os.path.exists(pdf_file_path):
                        with open(pdf_file_path, "rb") as f:
                            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                        
                        pdf_display_iframe = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" style="border: 1px solid rgba(255,255,255,0.05); border-radius: 8px;"></iframe>'
                        st.markdown(pdf_display_iframe, unsafe_allow_html=True)
                        
                        st.write("")
                        st.download_button(
                            label="📥 Download Tailored PDF Document",
                            data=open(pdf_file_path, "rb"),
                            file_name=os.path.basename(pdf_file_path),
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.error("Pipeline timeout. Please check your Ollama background status connection.")
    else:
        st.info("Fill out your technical profile entries on the workspace panel to execute the local AI builder pipeline.")