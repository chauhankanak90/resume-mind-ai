# llm.py

import os
import json
import requests
from prompt import get_ats_optimized_prompt

def generate_resume_data(name, contact, experience, projects, education, skills, certificates, job_description="", model_name="llama3"):
    prompt = get_ats_optimized_prompt(name, contact, experience, projects, education, skills, certificates, job_description)
    
    # 1. Agar cloud server par Groq Key milti hai, toh Cloud use karo
    if os.environ.get("GROQ_API_KEY"):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile", # <--- Groq ka sabse naya aur stable model yahan update kar diya hai
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
        
        if os.environ.get("GROQ_API_KEY"):
            return json.loads(res_json['choices'][0]['message']['content'])
        else:
            return json.loads(res_json['response'])
            
    except Exception as e:
        print(f"Error: {e}")
        return None