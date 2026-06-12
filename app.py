import streamlit as st
import PyPDF2
from groq import Groq
from dotenv import load_dotenv
import os

# Page Config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Sidebar
with st.sidebar:
    st.title("📄 Resume Analyzer")

    st.info("""
### Features

✅ Resume Score

✅ Skills Extraction

✅ Experience Summary

✅ Gap Analysis

✅ ATS Optimization

✅ AI Recommendations
""")

# Header
st.markdown(
    """
    <h1 class='main-title'>📄 RESUME ANALYZER</h1>
    <p class='subtitle'>
Upload your CV and receive a professional AI-powered analysis report.
</p>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<div class="welcome-container">

<h1 class="hero-title">
🚀 AI Resume Analyzer
</h1>

<p class="hero-text">
Get instant AI-powered resume analysis, ATS scoring, skill evaluation,
career recommendations, and professional insights to maximize your chances
of landing your dream job.
</p>

<div class="stats-container">

<div class="stat-card">
<h2>95%</h2>
<p>ATS Accuracy</p>
</div>

<div class="stat-card">
<h2>AI</h2>
<p>Powered Analysis</p>
</div>

<div class="stat-card">
<h2>24/7</h2>
<p>Instant Feedback</p>
</div>

</div>

</div>
""", unsafe_allow_html=True)

# Feature Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='metric-box'>
        <h3>🎯 ATS Score</h3>
        Resume Compatibility Analysis
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-box'>
        <h3>🧠 AI Insights</h3>
        Skills & Experience Evaluation
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='metric-box'>
        <h3>📈 Improvements</h3>
        Actionable Recommendations
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        resume_text = ""

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        st.success("✅ Resume Uploaded Successfully!")

        if st.button("Analyze Resume"):

            with st.spinner("Analyzing Resume..."):

                prompt = f"""
You are an expert HR Resume Analyzer.

Analyze the following resume and provide:

1. Candidate Name
2. Key Skills
3. Education Summary
4. Experience Summary
5. Resume Score (out of 100)
6. Strengths
7. Weaknesses
8. Missing Skills / Gaps Checklist
9. Improvement Suggestions
10. ATS Optimization Tips
11. Final Recommendation

Resume:
{resume_text}
"""

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3
                )

                result = response.choices[0].message.content

                st.subheader("📊 Resume Analysis Report")
                st.write(result)

    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("---")

st.markdown(
    """
    <div class='footer'>
        Built for your ease in finding jobs!
    </div>
    """,
    unsafe_allow_html=True
)
