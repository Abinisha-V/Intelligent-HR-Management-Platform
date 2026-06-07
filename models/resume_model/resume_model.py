# ================================
# Resume Screening Model using BERT
# ================================

# --------- IMPORT LIBRARIES ---------
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
import docx
import os

# --------- LOAD BERT MODEL (lazy loading) ---------
model = None

def get_model():
    global model
    if model is None:
        print("Loading BERT model for resume screening...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

# --------- FUNCTIONS ---------

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF resume using pypdf
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(docx_path):
    """
    Extract text from DOCX resume
    """
    doc = docx.Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return " ".join(full_text)


def get_resume_text(file_path):
    """
    Detect file type and extract text
    """
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")


def clean_text(text):
    """
    Basic text cleaning
    """
    text = text.lower()
    text = text.replace("\n", " ")
    return text


def resume_match_score(resume_text, job_skills_text):
    """
    Calculate BERT-based similarity score
    """
    bert_model = get_model()
    resume_text = clean_text(resume_text)
    job_skills_text = clean_text(job_skills_text)

    embeddings = bert_model.encode([resume_text, job_skills_text])

    similarity = cosine_similarity(
        [embeddings[0]], [embeddings[1]]
    )[0][0]

    return round(similarity * 100, 2)


# --------- MAIN PROGRAM ---------

if __name__ == "__main__":

    # 🔹 Path to resume file
    resume_file_path = "sample_resume.pdf"   # change if needed

    # 🔹 Job required skills (HR input)
    job_skills = """
    Python, SQL, Flask, Machine Learning, REST API,
    Backend Development, Data Analysis
    """

    if not os.path.exists(resume_file_path):
        print("[ERROR] Resume file not found!")
    else:
        resume_text = get_resume_text(resume_file_path)

        score = resume_match_score(resume_text, job_skills)

        print("Resume Match Result")
        print("----------------------")
        print(f"Match Percentage: {score}%")

        if score >= 75:
            print("Status: Shortlisted")
        elif score >= 50:
            print("Status: Maybe")
        else:
            print("Status: Rejected")
