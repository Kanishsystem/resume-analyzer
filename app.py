import streamlit as st
from utils.resume_parser import extract_text
from utils.analyzer import analyze_resume

st.set_page_config(page_title="Resume Analyzer", layout="wide")

st.title("📄 Resume Analyzer using Streamlit")
st.write("Upload your resume to get instant feedback and improvement suggestions!")

uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx","jpg", "jpeg", "png"],
                                 
                                 accept_multiple_files=True)

# if uploaded_file:
   
#     resume_text = extract_text(uploaded_file)

#     if resume_text:
#         st.subheader("Resume Preview")
#         st.text_area("Extracted Text", resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text, height=200)

        
#         result = analyze_resume(resume_text)

#         st.subheader("📊 Resume Analysis Report")
#         st.metric("Validation Score", f"{result['score']}%")
#         st.progress(result['score'] / 100)

#         st.write("### 🧠 Improvement Suggestions")
#         for key in result["improvements"]:
#             st.write(f"- {key}")
#     else:
#         st.error("Could not extract text from the resume. Please upload a valid file.")

if uploaded_file:
    all_text = ""

    for uploaded_file in uploaded_file:
        st.write(f"📂 Processing: **{uploaded_file.name}** ...")
        resume_text = extract_text(uploaded_file)
        all_text += "\n" + resume_text

    if all_text.strip():
        st.subheader("📝 Extracted Resume Text")
        st.text_area("Extracted Text", all_text[:1500] + "..." if len(all_text) > 1500 else all_text, height=250)

        # Analyze combined text
        result = analyze_resume(all_text)

        st.subheader("📊 Resume Analysis Report")
        st.metric("Validation Score", f"{result['score']}%")
        st.progress(result['score'] / 100)

        st.write("### 🧠 Improvement Suggestions")
        for key in result["improvements"]:
            st.write(f"- {key}")
    else:
        st.error("Could not extract text from the uploaded files. Please check formats.")
