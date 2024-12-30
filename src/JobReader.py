class JobReader:
    def __init__(self):
        self.jobs = []
    
    def read(self, content):
        self.jobs.append(content)