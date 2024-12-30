import os
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from collections import Counter
import re
import spacy
from config import JOB_DESCRIPTION_FILE, RESUME_PATH
import subprocess


def extract_texts_from_pdfs(resume_folder):
    texts = []
    for pdf_file in os.listdir(resume_folder):
        if pdf_file.endswith('.pdf'):
            text = extract_text(os.path.join(resume_folder, pdf_file))
            texts.append(text)
    return texts


def rank_resumes(job_description, resume_folder):
    
    nlp = spacy.load("en_core_web_sm") 

    def extract_name(text):
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Unknown"

    resumes = extract_texts_from_pdfs(resume_folder)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([job_description] + resumes)
    
    feature_names = vectorizer.get_feature_names_out()
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)
    #print(tfidf_df) #just to see the tfidf matrix

    for i in range(1, len(resumes) + 1):
        cosine_similarity_score = cosine_similarity(tfidf_df[0:1], tfidf_df[i:i+1]).flatten()[0]
        applicant_name = extract_name(resumes[i-1])  
        print(f"Resume {i} ({applicant_name}): {cosine_similarity_score}")


def get_job_description(file_path):
    with open(file_path, 'r') as file:
        job_description = file.read()
    return job_description

job_description = get_job_description(JOB_DESCRIPTION_FILE)
rank_resumes(job_description, RESUME_PATH)
