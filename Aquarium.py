import random, sys, time, bext

WIDTH, HEIGHT = bext.size()

WIDTH -= 1

NUM_KELP = 2
NUM_FISH = 10
NUM_BUBBLERS = 1
FRAMES_PER_SECOND = 4

FISH_TYPES = [
    {'right': ['><>'],              'left': ['<><']},
    {'right': ['>||>'],             'left': ['<||<']},
    {'right': ['>))>'],             'left': ['<((<']},
    {'right': ['>||o', '>||.'],     'left': ['o||<', '.||<']},
    {'right': ['>))o', '>)).'],     'left': ['o((<', '.((<']},
    {'right': ['>_==>'],            'left': ['<==_<']},
    {'right': [r'>\\>'],            'left': ['<//<']},
    {'right': ['><)))*>'],          'left': ['<*(((><']},
]

LONGEST_FISH_LENGTH = 10

LEFT_EDGE = 0
RIGHT_EDGE = WIDTH - 1 - LONGEST_FISH_LENGTH
TOP_EDGE = 0
BOTTOM_EDGE = HEIGHT - 2


def main():

    global FISHES, BUBBLERS, BUBBLES, KELPS, STEP

    bext.bg('black')
    bext.clear()

    FISHES = []
    for i in range(NUM_FISH):
        FISHES.append(generateFish())

    BUBBLERS = []
    for i in range(NUM_BUBBLERS):
        BUBBLERS.append(random.randint(LEFT_EDGE, RIGHT_EDGE))
    BUBBLES = []

    KELPS = []
    for i in range(NUM_KELP):
        kelpx = random.randint(LEFT_EDGE, RIGHT_EDGE)
        kelp = {'x': kelpx, 'segments': []}
        for i in range(random.randint(6, HEIGHT-1)):
            kelp['segments'].append(random.choice(['(', ')']))
        KELPS.append(kelp)

    STEP = 1
    while True:
        simulateAquarium()
        drawAquarium()
        time.sleep(1/FRAMES_PER_SECOND)
        clearAquarium()
        STEP += 1


def getRandomColor():
    return random.choice(('black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'))


def generateFish():
    fishType = random.choice(FISH_TYPES)
    colorPattern = random.choice(('random', 'head-tail', 'single'))
    fishLength = len(fishType['right'][0])
    if colorPattern == 'random':
        colors = []
        for i in range(fishLength):
            colors.append(getRandomColor())
    if colorPattern == 'single' or colorPattern == 'head-tail':
        colors = [getRandomColor()] * fishLength
    if colorPattern == 'head-tail':
        headTailColor = getRandomColor()
        colors[0] = headTailColor
        colors[-1] = headTailColor

    fish = {'right': fishType['right'],
            'left': fishType['left'],
            'colors': colors,
            'hSpeed': random.randint(1, 6),
            'vSpeed': random.randint(5, 15),
            'timeToHDirChange': random.randint(10, 60),
            'timeToVDirChange': random.randint(2, 20),
            'goingRight': random.choice([True, False]),
            'goingDown': random.choice([True, False])
    }

    fish['x'] = random.randint(0, WIDTH - 1 - LONGEST_FISH_LENGTH)
    fish['y'] = random.randint(0, HEIGHT - 2)

    return fish


def simulateAquarium():

    global FISHES, BUBBLERS, BUBBLES, KELP, STEP

    for fish in FISHES:
        if STEP % fish['hSpeed'] == 0:
            if fish['goingRight']:
                if fish['x'] != RIGHT_EDGE:
                    fish['x'] += 1
                else:
                    fish['goingRight'] == False
                    fish['colors'].reverse()
            else:
                if fish['x'] != LEFT_EDGE:
                    fish['x'] -= 1
                else:
                    fish['goingRight'] = True
                    fish['colors'].reverse()
                    
