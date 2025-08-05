class GameState:
    def __init__(self):
        self.score = 0
        self.timer = ''
        self.target = (150, 350)
        self.quit = False
        self.restart = False
        self.counter = 0
        self.frame_idx = 0
        self.gif_frames = []
