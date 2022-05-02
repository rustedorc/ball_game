FPS = 60
WIDTH = 800
HEIGHT = 600
CAPTION = 'Ball Game'

COLOURS = {'black':(0,0,0),
'white' : (255, 255, 255),
'yellow': (255, 255, 0),
'purple': (255, 0, 255),
'green': (0, 255, 0),
'red': (255, 0, 0),
'blue':(0,0, 255)}

BALL_COLOURS = {key:value for key, value in COLOURS.items() if key != 'black'}

GRAVITY = HEIGHT / (FPS ** 2)
SPEED_MULTIPLIER = 5
ENERGY_LOSS = 0.95