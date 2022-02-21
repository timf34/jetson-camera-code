import cv2 
import typing 

# Note: look into type hinting 

class JetsonCamera():
    def __init__(self, width: int=1980, height: int=1080):
        self.width = width 
        self.height = height

    


def test():
    jc = JetsonCamera()
    print(jc.width)

if __name__ == '__main__':
    test()