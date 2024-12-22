from pathlib import Path

class OpticalCharacterRecognition:
    def __init__(self, config, workdir):
        self.config = config
        if workdir is not None: 
            self.workdir = Path(workdir)
            if self.workdir.exists() == False:
                raise Exception(f"{workdir} does not exist!!")
        else:
            self.workdir = Path('')
        self.text = ''
        self.ocrEngine = ocrEngine.
    

