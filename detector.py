import cvlib
import cv2
from db import config

class Detector:
    def __init__(self):
          self.model = list(config(section="yolo").values())[0]
    
    def detectBirds(self, file):
        # image = cv2.imread(file[1:])
        # _, label, _ = cvlib.detect_common_objects(image, model=self.model)
        # birds = label.count('bird')
        # if birds == 0 or birds > 1:
        #     return False
        # else: return True
        return True