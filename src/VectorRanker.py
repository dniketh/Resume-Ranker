from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class VectorRanker:
    def __init__(self, 
                job,
                resume_list,
                vectorizer = None):
        self.vectorizer = self._get_vectorizer(vectorizer)
        self.job = job
        self.resume_list = resume_list

    def _get_vectorizer(self, vectorizer):
        if vectorizer == None:
            return TfidfVectorizer()
    
    def vectorize(self):
        resumes = [data[1] for data in self.resume_list]
        self.X = self.vectorizer.fit_transform([self.job] + resumes)
        return self.X
    
    def rank(self):
        job_matrix = self.X.toarray()[0].reshape(1,-1)
        resume_matrix = self.X.toarray()[1:]
        cos_sim = cosine_similarity(job_matrix, resume_matrix).flatten()
        self.sorted_indices = np.argsort(cos_sim)[::-1]
    
    def get_t1_resume(self):
        return self.resume_list[0][0]
