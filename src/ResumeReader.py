import os

class ResumeReader:
    def __init__(self, path, vectorizer, algo):
        self.path = path
        self.vectorizer = vectorizer
        self.algo = algo
        self.resumesContent = []
        self.resumeName = []
    
    def _get_from_pdf(self, file_path):
        return self.algo.extract_text(file_path) 

    def _get_from_docx(self):
        raise NotImplementedError("Docx are not supported as the moment")
    
    def get_texts(self):
        pdfs = []
        docxs = []

        for file in os.listdir(self.path):
            if file.endswith('.pdf'):
                pdfs.append(file)
            else:
                docxs.append(file)
        
        for pdf in pdfs:
            pdf_path = os.path.join(self.path, pdf)
            self.resumeName.append(pdf_path)
            self.resumesContent.append(self._get_from_pdf(pdf_path))
       
        # for docx in docxs:

        #     self.resumes.append(self._get_from_docx(os.path.join(self.path, pdf)))
        return self.resumesContent
       