import streamlit as st
from utils.resume_parser import extract_text
from utils.analyzer import analyze_resume
from PIL import Image
import plotly.graph_objects as go

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

# ----------------------------- #
# Custom CSS for styling
# ----------------------------- #
st.markdown("""
    <style>
    .center { display: flex; justify-content: center; align-items: center; flex-direction: column; }
    .title { text-align: center; font-size: 2rem; color: #2E86C1; font-weight: bold; margin-top: -10px; }
    .subtitle { text-align: center; color: gray; font-size: 1rem; margin-bottom: 20px; }
    .stFileUploader { border: 2px dashed #2E86C1 !important; padding: 20px; border-radius: 15px; background-color: #f7faff; }
    div[data-testid="stMetricValue"] { color: #27AE60; font-weight: bold; font-size: 1.6rem; }

    /* 🌈 Animated gradient background */
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #e3f2fd, #fce4ec, #f3e5f5, #e8f5e9);
        background-size: 400% 400%;
        animation: gradientMove 15s ease infinite;
    }

    /* Optional: make app cards and boxes pop */
    .stFileUploader, .stTextArea, .stMetric, .stPlotlyChart {
        background: rgba(255,255,255,0.8);
        border-radius: 12px;
        padding: 10px;
        backdrop-filter: blur(4px);
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------- #
# Header Section
# ----------------------------- #
with st.container():
    st.markdown('<div class="center">', unsafe_allow_html=True)
    logo = Image.open("logo.png")
    st.image(logo, width=220)
    st.markdown('<h1 class="title">📄 Resume Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload your resume and get AI-powered feedback & suggestions instantly</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- #
# File Upload Section
# ----------------------------- #
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_file:
    all_text = ""
    invalid_files = []

    for file in uploaded_file:
        st.write(f"📂 Processing: **{file.name}** ...")
        try:
            resume_text = extract_text(file)

            # Check if resume text is empty or too short
            if not resume_text or len(resume_text.strip()) < 50:
                invalid_files.append(file.name)
            else:
                all_text += "\n" + resume_text

        except Exception as e:
            invalid_files.append(file.name)
            st.error(f"❌ Error reading {file.name}: {e}")

    # Show warnings if invalid files were found
    if invalid_files:
        st.warning(
            f"⚠️ The following files could not be processed or contain unreadable content:\n"
            + "\n".join([f"- {name}" for name in invalid_files])
        )

    # Show summary status
    if invalid_files:
        st.markdown(
            "<p style='color: #e74c3c; font-weight:bold;'>⚠️ Some files were invalid!</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<p style='color: #27ae60; font-weight:bold;'>✅ All files processed successfully!</p>",
            unsafe_allow_html=True
        )

    # ----------------------------- #
    # Analyze valid resumes
    # ----------------------------- #
    if all_text.strip():
        st.subheader("📝 Extracted Resume Text")
        st.text_area(
            "Extracted Text",
            all_text[:1500] + "..." if len(all_text) > 1500 else all_text,
            height=250
        )

        # Run analyzer
        result = analyze_resume(all_text)

        st.subheader("📊 Resume Analysis Report")
        st.metric("Detected Stream", result["stream"])
        st.metric("Validation Score", f"{result['total']}%")
        st.progress(result['total'] / 100)

        # ----------------------------- #
        # Resume Completeness Chart
        # ----------------------------- #
        st.subheader("📈 Resume Section Completeness")

        sections = ["Objective", "Skills", "Experience", "Education", "Projects"]
        values = [
            100 if any(word in all_text.lower() for word in ["objective", "summary", "professional summary"]) else 0,
            100 if "skills" in all_text.lower() else 0,
            100 if "experience" in all_text.lower() else 0,
            100 if "education" in all_text.lower() else 0,
            100 if "project" in all_text.lower() else 0
        ]

        fig = go.Figure(data=[
            go.Bar(
                x=sections,
                y=values,
                text=[f"{v}%" for v in values],
                textposition='auto',
                marker_color=['#3498db', '#1abc9c', '#9b59b6', '#f39c12', '#e74c3c']
            )
        ])

        fig.update_layout(
            yaxis=dict(title="Completeness (%)", range=[0, 100]),
            xaxis=dict(title="Resume Sections"),
            title="Your Resume Coverage by Section",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # ----------------------------- #
        # Suggestions
        # ----------------------------- #
        st.write("### 🧠 Suggestions for Improvement")
        for key in result["suggestions"]:
            st.write(f"- {key}")

    else:
        st.error("🚫 No valid resumes could be processed. Please upload a proper PDF or DOCX file.")
