from PIL import Image
from random import randint

class BalloonGifs:
    def importGif(self, path):
        gif = Image.open(path)
        gif_frames = []
        try:
            while True:
                frame = gif.convert("RGBA")  # Support transparency
                resized_frame =frame.copy().resize((100,120))
                gif_frames.append(resized_frame)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        finally:
            return gif_frames
    def __init__(self):
        self.blue=self.importGif("blue-balloon.gif")
        self.red=self.importGif("red-balloon.gif")
        self.green=self.importGif("green-balloon.gif")
        self.balloons=[self.red,self.blue,self.green]

    def getRandomBalloon(self):
        return self.balloons[randint(0,2)]