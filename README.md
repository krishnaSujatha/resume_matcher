# Resume Matcher

Resume Matcher is a Streamlit application that allows users to upload resumes and job descriptions, and then computes the similarity between them using cosine similarity. The application highlights matched resumes in green and not matched resumes in red.

## Features

- Upload multiple resumes in PDF format.
- Upload or type a job description.
- Compute similarity scores between resumes and job descriptions.
- Display results in a table with conditional formatting.
- Custom CSS styling for a better user experience.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/resume-matcher.git
    cd resume-matcher
    ```

2. Create a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:

    ```sh
    streamlit run main.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Upload your resumes and job description, set the matching score, and click the "Match" button to see the results.

## Project Structure
