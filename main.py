import streamlit as st
from utilities import extract_text_from_pdf, compute_similiarity
import pandas as pd

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #e8f0fe;
    }
    .stTextArea>div>div>textarea {
        background-color: #e8f0fe;
    }
    .stNumberInput>div>div>input {
        background-color: #e8f0fe;
    }
    .stFileUploader>div>div>div>button {
        background-color: #4CAF50;
        color: white;
    }
    .stTable>table {
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-collapse: collapse;
        width: 100%;
    }
    .stTable>table>thead>tr>th {
        background-color: #4CAF50;
        color: white;
        padding: 8px;
    }
    .stTable>table>tbody>tr>td {
        padding: 8px;
        border: 1px solid #ddd;
    }
    .title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
    }
    .subtitle {
        font-size: 20px;
        font-weight: bold;
    }
    .info-title {
        font-size: 18px;
        font-weight: bold;
    }
    .matched {
        background-color: #d4edda;
        color: #155724;
    }
    .not-matched {
        background-color: #f8d7da;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Resume Matcher</div>', unsafe_allow_html=True)

st.markdown('<div class="info-title">Set Matching Score</div>', unsafe_allow_html=True)
matching_score = st.number_input("", min_value=0.0, max_value=100.0, value=50.0)
matching_score = matching_score / 100

# Upload multiple resumes
st.markdown('<div class="info-title">Upload your resumes (PDF)</div>', unsafe_allow_html=True)
uploaded_files = st.file_uploader("", type="pdf", accept_multiple_files=True)

def get_sample_job_description():
    """Return a sample job description."""
    return """4 years of experience in designing, developing, testing, and implementing a wide range of Internet-based
applications with analytical, design, and development skills.
✓ Proficient in Python, Flask and other programming languages and platforms.
✓ Proven experience delivering high-quality deliverables on time using Agile or Waterfall methodologies during the
.
"""

# Upload job description or type it
st.markdown('<div class="info-title">Upload job description (PDF)</div>', unsafe_allow_html=True)
uploaded_jd = st.file_uploader("", type="pdf")

# Initialize session state for typed job description
if 'typed_jd' not in st.session_state:
    st.session_state.typed_jd = ""

# Clear typed job description if a PDF is uploaded
if uploaded_jd is not None:
    st.session_state.typed_jd = ""

# Disable the default job description checkbox and empty the text box if a PDF is uploaded
if uploaded_jd is not None:
    use_default_jd = False
    st.markdown('<div class="info-title">Or type job description</div>', unsafe_allow_html=True)
    typed_jd = st.text_area("", value=st.session_state.typed_jd, disabled=True)
else:
    # Checkbox to use default job description
    use_default_jd = st.checkbox("Use default job description")
    
    # Pre-fill the text area with the sample job description if the checkbox is selected
    st.markdown('<div class="info-title">Or type job description</div>', unsafe_allow_html=True)
    if use_default_jd:
        typed_jd = st.text_area("", value=get_sample_job_description())
    else:
        typed_jd = st.text_area("", value=st.session_state.typed_jd)

# Add a button to start the matching process
if st.button("Match"):
    if uploaded_files:
        # Check if job description is provided
        if uploaded_jd is None and not typed_jd and not use_default_jd:
            st.warning("Please upload, type, or select a job description.")
        else:
            # Check for duplicate resume names
            resume_names = [file.name for file in uploaded_files]
            if len(resume_names) != len(set(resume_names)):
                st.error("Duplicate resume names found. Please upload resumes with unique names.")
            else:
                # Extract text from the uploaded job description PDF or use typed job description
                if uploaded_jd is not None:
                    jd_text = extract_text_from_pdf(uploaded_jd)
                elif typed_jd:
                    jd_text = typed_jd
                else:
                    jd_text = get_sample_job_description()
                
                # Initialize a list to store results
                results = []

                # Process each uploaded resume
                for uploaded_file in uploaded_files:
                    resume_text = extract_text_from_pdf(uploaded_file)
                    similarity_score = compute_similiarity(resume_text, jd_text)
                    if similarity_score >= matching_score:
                        match_val = "Matched"
                        match_class = "matched"
                    else:
                        match_val = "Not Matched"
                        match_class = "not-matched"
                    results.append({"Resume Name": uploaded_file.name, "Similarity Score": similarity_score, "Match": match_val,})
                
                # Convert results to DataFrame for better display
                results_df = pd.DataFrame(results)
                
                # Apply conditional formatting to the DataFrame
                def highlight_rows(row):
                    if row['Match'] == 'Matched':
                        return ['background-color: #d4edda; color: #155724'] * len(row)
                    else:
                        return ['background-color: #f8d7da; color: #721c24'] * len(row)
                
                styled_df = results_df.style.apply(highlight_rows, axis=1)
                
                # Display results in a table with conditional formatting
                st.markdown('<div class="subtitle">Similarity Scores</div>', unsafe_allow_html=True)
                st.dataframe(styled_df)
    else:
        st.error("Please upload at least one resume.")