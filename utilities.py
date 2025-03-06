import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import fitz
from sentence_transformers import SentenceTransformer    #### BERT model

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Load pre-trained Sentence-BERT model
def compute_similiarity(resume_text, jd_text):
  "this function checks cosine similiarty by using cosine function"
  resume_embedding = get_embedding(resume_text)
  jb_embedding = get_embedding(jd_text)
  similarity_score = cosine_similarity(
      [resume_embedding], [jb_embedding]
  ) [0][0]
  return similarity_score


def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def get_embedding(text):
    """Convert text to BERT embeddings."""
    return model.encode([text])[0]
