import cvlib
import cv2

class Detector:
    def __init__(self,detection_model:str):
          self.model = detection_model
    
    def detectBirds(self, file):
        image = cv2.imread(file[1:])
        _, label, _ = cvlib.detect_common_objects(image, model=self.model)
        birds = label.count('bird')
        if birds == 0 or birds > 1:
            return False
        else: return True