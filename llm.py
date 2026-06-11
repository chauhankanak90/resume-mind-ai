# llm.py

import os
import json
import requests
import streamlit as st  # Streamlit import kiya secrets check karne ke liye
from prompt import get_ats_optimized_prompt

def generate_resume_data(name, contact, experience, projects, education, skills, certificates, job_description="", model_name="llama3"):
    prompt = get_ats_optimized_prompt(name, contact, experience, projects, education, skills, certificates, job_description)
    
    # Streamlit Cloud ke Secrets check karne ka native tarika
    groq_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    
    # 1. Agar cloud server par Groq Key milti hai, toh Cloud use karo
    if groq_key:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }
    # 2. Agar key nahi milti (jaise aapke localhost par), toh purana Ollama chalega
    else:
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
        res_json = response.json()
        
        if groq_key:
            return json.loads(res_json['choices'][0]['message']['content'])
        else:
            return json.loads(res_json['response'])
            
    except Exception as e:
        print(f"Error: {e}")
        return None