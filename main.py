import pygame, random, math, sys, os, copy
from pygame.locals import *

def vmag(vectorToMag):
    partialSum = 0
    for i in vectorToMag:
        partialSum += math.pow(i, 2)
    return math.sqrt(partialSum)

def vsub(vecOne, vecTwo):
    assert(len(vecOne) == len(vecTwo)), 'to substract vectors they must have the same number of dimensions'
    vecFinal = vecOne.copy()
    for i in range(0, len(vecFinal)):
        vecFinal[i] -= vecTwo[i]
    return vecFinal

def vmult(scalarPart, vectorPart):
    #print(scalarPart, '*', vectorPart)
    for i in range(0, len(vectorPart)):
        vectorPart[i] *= scalarPart
    #print(vectorPart)
    return vectorPart

def readFile(fileToRead):
    print(fileToRead)
    currentFile = open(fileToRead, 'r')
    output = currentFile.readlines()
    #print(output)
    return(output)

def bounder(minner, valueRun, maxer):
    #print(minner, valueRun, maxer, int(max(min(valueRun, maxer), minner)))
    return max(min(valueRun, maxer), minner)


FPS = 60
FPSCLOCK = pygame.time.Clock()
dispsurf = pygame.display.set_mode((1530, 530), pygame.RESIZABLE)
hudsurf = pygame.Surface((1530, 530))
#res = dispsurf.get_size()

levels = [
    'maps/1',
    'maps/2',
    'maps/3',
    'maps/4',
    'maps/5'
]
validTiles = os.listdir('tiles/')
surf00 = pygame.image.load('hud/00.png')
surf02 = pygame.image.load('hud/02.png')
surf20 = pygame.image.load('hud/20.png')
surf22 = pygame.image.load('hud/22.png')
surf01 = pygame.image.load('hud/01.png')
surf10 = pygame.image.load('hud/10.png')


keyStates = []
loadedTiles = {}
tileSize = 16
for i in range(0, 400):
    keyStates.append(False)

tileProperties = {
    'g': (True, .25, .015, .35, {'slowdamage': .10, 'splat': .15}),
    'i': (True, 1.1, .05, .0001, {'splat': .5}),
    'w': (False, .025, .5),
    'r': (True, .25, .005, .7, {'slowdamage': .25, 'splat': .75}),
    'b': (False, 1, 0),
    'k': (False, .0001, 2),
    'c': (True, .5, .025, .015, {'damage': 20}),
    's': (True, .15, .0025, .5, {'splat': .05}),
    'm': (True, 1.1, .05, .001, {'angle': 30, 'splat': .0}),
    'p': (True, .5, .025, .015, {'portal': True}),
    'h': (True, 1, .015, .15, {'help': True}),
    'f': (True, 20, 3, 0, {'splat': .5}),
    'z': (False, 1.2, 0)
    #'g': ()
    #'g': ()
}

weaponStats = {
    'sword': (2, 40, 60),
    'spear': (4, 30, 90),
    'axe': (1.5, 60, 120)
}

lastPos = 5

def surfaceOf(textToSurf):
    #print(textToSurf)
    if textToSurf in loadedTiles:
        return loadedTiles[textToSurf]
    if textToSurf + '.png' in validTiles:
        loadedTiles[textToSurf] = pygame.transform.scale(pygame.image.load('tiles/' + textToSurf + '.png'), (tileSize, tileSize))
        return loadedTiles[textToSurf]
    else:
        return pygame.Surface((tileSize, tileSize))

mapperNow, subSurf, worldSurf, currentSpot, playerSpot, enemies, helps, items, enweps = 0, 0, 0, 0, 0, [], [], [], []

def newLevel(levelText):
    #print('stering')
    global mapperNow, subSurf, worldSurf, currentSpot, playerSpot, enemies, helps, items, enweps
    mapperNow, subSurf, worldSurf, currentSpot, playerSpot, enemies, helps, items, enweps = 0, 0, 0, 0, 0, [], [], [], []
    mapperNow = readFile(levelText + '/main.txt')
    subSurf = pygame.Surface(((len(mapperNow[0]) + 1) * tileSize, (len(mapperNow) + 2) * tileSize))
    for i in range(0, len(mapperNow[0]) - 1):
        for j in range(0, len(mapperNow)):
            #print(i, j)
            #effectiveSpot = ((currentSpot[0] + int(dispRes[0] / 2) - i), int(currentSpot[1] + (dispRes[1] / 2) - j))
            pygame.draw.rect(subSurf, (0, 255, 255), (i * tileSize, j * tileSize, 5, 5))
            subSurf.blit(
                surfaceOf(
                    mapperNow[j][i]
                ),
                    (
                        (i * tileSize),
                        (j * tileSize)
                    )
                )
    print('rendered?', subSurf.get_size())
    worldSurf = subSurf.copy()
    currentSpot = [20, 20]
    playerSpot = [20, 20]
    exter = readFile(levelText + '/extras.txt')
    brackets = []
    for i in range(0, len(exter)):
        brackets.append(0)
        if exter[i].__contains__('{'):
            brackets[i] += 1
        if exter[i].__contains__('}'):
            brackets[i] -= 1
    enemyEndSpot = 0
    enemyStartSpot = 0
    iteratoer = 0
    while enemyStartSpot == 0:
        if brackets[iteratoer] == 1:
            enemyStartSpot = iteratoer
        iteratoer += 1
    #iteratoer += 1
    summae = 1
    while enemyEndSpot == 0:
        summae += brackets[iteratoer]
        if summae == 0:
            enemyEndSpot = iteratoer
        iteratoer += 1
    for i in range(enemyStartSpot + 1, enemyEndSpot):
        if brackets[i] == 1:
            enemies.append([i])
            enweps.append([i])
        if brackets[i] == -1:
            enemies[len(enemies) - 1].append(i)
            enweps[len(enweps) - 1] = exter[i + 1].strip()
    #print(enemies)
    for i in range(0, len(enemies)):
        #print(enemies[i], 'heeey', enemies[i][1])
        nows = enemies[i][0]
        nowe = enemies[i][1]
        enemies[i] = []
        for j in range(nows + 1, nowe):
            enemies[i].append([0,0])
            #print(enemies[i])
            partialProcess = exter[j][exter[j].index('(') + 1:]
            enemies[i][j - nows - 1][0] = int(partialProcess[:partialProcess.index(')')])
            partialProcess = partialProcess[partialProcess.index('(') + 1:]
            #print(enemies[i], partialProcess, partialProcess.index(')'), partialProcess[:partialProcess.index(')')])
            err = partialProcess[:partialProcess.index(')')]
            enemies[i][j - nows - 1][1] = int(err)
        #print(enemies, enweps)

def tilesOn(inputRect):
    #print(inputRect, 'crashtime')
    tilesReturned = []
    dimensCheck = (math.ceil(inputRect[2] / tileSize) + 1, math.ceil(inputRect[3] / tileSize) + 1)
    topCheck = (math.floor(inputRect[0] / tileSize), math.floor(inputRect[1] / tileSize))
    lastAppend = 't'
    for i in range(topCheck[0], topCheck[0] + dimensCheck[0]):
        tilesReturned.append([])
        for j in range(topCheck[1], topCheck[1] + dimensCheck[1]):
            #print(j, i)
            thingGrabbed = mapperNow[bounder(0, j, len(mapperNow) - 1)][bounder(0, i, len(mapperNow[0]) - 1)]
            if(thingGrabbed in tileProperties):
                tilesReturned[len(tilesReturned) - 1].append(thingGrabbed)
                lastAppend = thingGrabbed
            else:
                tilesReturned[len(tilesReturned) - 1].append(lastAppend)
    #print(dimensCheck, topCheck)
    return tilesReturned

class entitySprite(pygame.sprite.Sprite):
    def __init__(self, h = 100, s = [10, 10, 0], w = False):
        super().__init__()
        self.velo = [0, 0, 0]
        self.health = h
        self.pos = s
        self.priorSpeed = [0, 0, 0]
        self.preorSpeed = [0, 0, 0]
        self.weapon = w
        self.attackCool = 0
        self.damageCool = 0

    def update(self):
        self.attackCool, self.damageCool = max(0, self.attackCool - 1), max(0, self.damageCool - 1)
        self.move()
        self.trueRect[0], self.trueRect[1] = (self.pos[0]) * tileSize, (self.pos[1]) * tileSize
        scaleConstant = math.asin(1 /(2 * (10 - min(9.5, self.pos[2])))) / math.asin(1 /(20))
        #print(scaleConstant)
        self.rect = self.trueRect.copy()
        self.rect[2] *= scaleConstant
        self.rect[3] *= scaleConstant
        self.image = pygame.transform.scale(self.image, (self.rect[2], self.rect[3]))
        self.rect[0] = self.rect[0] - (self.rect[2] - self.trueRect[2]) / 2
        self.rect[1] -= (self.rect[3] - self.trueRect[3]) / 2
        currentTiles = tilesOn(self.trueRect)
        for i in currentTiles:
            for j in i:
                if tileProperties[j][0]:
                    if 'damage' in tileProperties[j][4] and self.pos[2] == 0:
                        self.health -= tileProperties[j][4]['damage']
                        return
        #if(self.velo[2] != 0): print(self.velo[2], self.pos[2], scaleConstant, self.rect, self.trueRect)


    def crash(self, inputRect):
        # spdStart = vmag(playerSpeed)
        #print(inputRect)
        #priorSpeed = self.velo.copy()
        currentTiles = tilesOn(inputRect)
        #drawPix(inputRect)
        collisionPoints = [0, 0]
        if (not tileProperties[currentTiles[0][0]][0]):
            # print('00')
            collisionPoints[0] += 1
            collisionPoints[1] += 1
        if (not tileProperties[currentTiles[0][1]][0]):
            # print('01')
            collisionPoints[0] += 1
            collisionPoints[1] += -1
        if (not tileProperties[currentTiles[1][0]][0]):
            # print('10')
            collisionPoints[0] += -1
            collisionPoints[1] += 1
        if (not tileProperties[currentTiles[1][1]][0]):
            # print('11')
            collisionPoints[0] += -1
            collisionPoints[1] += -1
        if vmag(collisionPoints) == 0:
            #print('no crash on', inputRect)
            return False
        #print(collisionPoints, inputRect)
        for i in range(0, len(collisionPoints)):
            if abs(collisionPoints[i]) > 1:
                collisionPoints[i] /= abs(collisionPoints[i])
        aggregate = [0, 0, 0]
        for i in range(0, len(currentTiles)):
            for j in range(0, len(currentTiles[i])):
                if (not tileProperties[currentTiles[i][j]][0]):
                    aggregate[1] = (aggregate[1] * aggregate[0] + tileProperties[currentTiles[i][j]][1]) / (
                                aggregate[0] + 1)
                    aggregate[2] = (aggregate[2] * aggregate[0] + tileProperties[currentTiles[i][j]][2]) / (
                                aggregate[0] + 1)
                    aggregate[0] += 1
                    # print(aggregate)
        simulSpeed = [self.velo[0], self.velo[1]]
        #print('rn simul is ', simulSpeed, 'player is', self.velo)
        simulSpeed = vmult(aggregate[1], simulSpeed)
        #print(collisionPoints, simulSpeed)
        for i in range(0, len(simulSpeed)):
            simulSpeed[i] = abs(simulSpeed[i]) * collisionPoints[i]
            # print(simulSpeed)
            if abs(collisionPoints[i] + self.velo[i]) != abs(abs(collisionPoints[i]) + abs(self.velo[i])):
                if(self.colSpot[i] == -1):
                    self.colSpot[i] = inputRect[i] / tileSize
                    #print('should be', i, self.colSpot)
                    self.lastVelo[i] = self.velo[i]
                    #print(self.lastVelo, 'LASTVELOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
                    self.velo[i] = simulSpeed[i]
        if abs(self.velo[0]) < .005: self.velo[0] = 0
        if abs(self.velo[1]) < .005: self.velo[1] = 0
        #print(self.velo)
        # #print(simulSpeed)
        #print('lost', abs(vmag(self.velo) - vmag(simulSpeed)), 'with velo/simspeed/collisionpoints', self.velo, simulSpeed, collisionPoints)
        # if(vmag(playerSpeed) != spdStart):
        #     #print(collisionPoints, currentTiles)
        #print(self.velo)
        #print('crash on', inputRect, 'against', currentTiles, '----------------------------------------------------')
        #print(self.lastVelo, 'spooooooooooooooooooot')
        #print(priorSpeed, self.velo)x
        self.health -= max(min((vmag(self.priorSpeed) - vmag(self.velo)) * aggregate[2] * 40, (vmag(self.preorSpeed) - vmag(self.velo)) * aggregate[2] * 50)
, 0)
        #print(self.health)
        return True

    def findCollide(self, veloUse, recurse):
        simRect = self.trueRect.copy()
        dx = veloUse[0] * tileSize
        dy = veloUse[1] * tileSize
        self.colSpot = [-1, -1]
        if(not recurse): self.lastVelo = [False, False]
        if dx == 0 and veloUse[0] != 0:
            dx = veloUse[0] / abs(veloUse[0])
        if dy == 0 and veloUse[1] != 0:
            dy = veloUse[1] / abs(veloUse[1])
        simRect[0], simRect[1] = simRect[0] + dx, simRect[1] + dy
        #print('collideCheck', dx, dy, simRect, self.trueRect)
        #print(self.velo)
        #print('props:', dx, dy)
        if abs(dy) > abs(dx):
            for i in range(self.trueRect[1], simRect[1]):
                #print(i, 'y', (self.trueRect[0] + ((i - self.trueRect[1]) * dx / dy)), i)
                self.crash(((self.trueRect[0] + ((i - self.trueRect[1]) * dx / dy)), i, self.trueRect[2], self.trueRect[3]))
            for i in range(self.trueRect[1], simRect[1], -1):
                #print(i, 'y', (self.trueRect[0] + ((i - self.trueRect[1]) * dx / dy)), i)
                self.crash(((self.trueRect[0] + ((i - self.trueRect[1]) * dx / dy)), i, self.trueRect[2], self.trueRect[3]))
        else:
            #print('goin x')
            for i in range(self.trueRect[0], simRect[0]):
                #print(i, 'x', i, (self.trueRect[1] + ((i - self.trueRect[0]) * dy / dx)))
                self.crash((i, (self.trueRect[1] + ((i - self.trueRect[0]) * dy / dx)), self.trueRect[2], self.trueRect[3]))
            for i in range(self.trueRect[0], simRect[0], -1):
                #print(i, 'x', i, (self.trueRect[1] + ((i - self.trueRect[0]) * dy / dx)))
                self.crash((i, (self.trueRect[1] + ((i - self.trueRect[0]) * dy / dx)), self.trueRect[2], self.trueRect[3]))
        #print('boyob')
        hasCrashed = False
        nextVelo = veloUse.copy()
        for i in range(0, len(self.colSpot)):
            if self.colSpot[i] != -1:
                #print('boyoyoyo', self.colSpot)
                hasCrashed = True
                nextVelo[i] = (self.colSpot[i] - self.pos[i]) / self.lastVelo[i]
                self.pos[i] = self.colSpot[i]
                #print(self.pos, self.velo)
        #print('simmedcrash with', veloUse)
        if(hasCrashed):
            #print('crashed with usevlo', veloUse)
            if(self.velo[0] != veloUse[0] or self.velo[1] != veloUse[1]):
                #print('man!', self.velo, self.lastVelo, nextVelo)
                self.velo[0], self.velo[1] = .65 * self.lastVelo[0], .65 * self.lastVelo[1]
            for i in range(0, len(self.colSpot)):
                if self.colSpot[i] != -1:
                    nextVelo[i] *= self.velo[i]
            #print('goin with', nextVelo, 'from', self.colSpot, self.pos, self.lastVelo, self.velo)
            if(not self.findCollide(nextVelo, True)):
                self.pos[0] += nextVelo[0]
                self.pos[1] += nextVelo[1]
        #print(self.lastVelo, hasCrashed, 'FINDCOLLLLLLLLLLLLLLLLLL')
        return hasCrashed
        #print('boyod')


    def move(self):
        #prespot = self.pos.copy()
        self.preorSpeed = self.velo.copy()
        crashed = self.findCollide(self.velo, False)
        #print(self.lastVelo)
        #print('moving with', self.velo)
        if(not crashed):
            #print('x')
            self.pos[0] += self.velo[0]
        #else: print('x overrid')
        if(not crashed):
            #print('y')
            self.pos[1] += self.velo[1]
        #else: print('y overrid')
        #print(self.pos, prespot)
        self.pos[2] = max(0, self.pos[2] + self.velo[2])
        self.priorSpeed = self.velo.copy()
        # print(currentSpot, playerSpot, 'donemove')

    def accel(self, directionInput):
        #print('accelled')
        currentTiles = tilesOn(self.trueRect)
        #print('accelCalled', currentTiles)
        directionUse = [0, 0]
        aggregate = [0, 0, 0, 0, {}]
        if(self.pos[2] > 0):
            #print('hey')
            self.velo[2] -= .025
            return
        if(self.pos[2] == 0 and self.velo[2] != 0):
            splatter = [0, 0]
            for i in range(0, len(currentTiles)):
                for j in range(0, len(currentTiles[i])):
                    if tileProperties[currentTiles[i][j]][0]:
                        if 'splat' in tileProperties[currentTiles[i][j]][4]:
                            splatter[1] = ((splatter[1] * splatter[0]) + (tileProperties[currentTiles[i][j]][4]['splat'])) / (splatter[0] + 1)
                            splatter[0] += 1
            self.velo[2] = 0
        for i in range(0, len(currentTiles)):
            for j in range(0, len(currentTiles[i])):
                if not tileProperties[currentTiles[i][j]][0]:
                    # print('uh oh!', 'stinky!')
                    continue
                    # print('precall plays', playerSpeed)
                    # playerCrash(player.rect)
                    # return
                for k in range(1, 4):
                    aggregate[k] = ((aggregate[k] * aggregate[0]) + tileProperties[currentTiles[i][j]][k]) / (
                                aggregate[0] + 1)
                for k, v in tileProperties[currentTiles[i][j]][4].items():
                    aggregate[4][k] = v
                aggregate[0] += 1
        # print(aggregate)
        if vmag(self.velo) > aggregate[1]:
            # print('decel starting at', playerSpeed, 'using', currentTiles, 'avgs', aggregate)
            preSpeed = self.velo.copy()
            directionUse[0] = self.velo[0]
            directionUse[1] = self.velo[1]
            if (directionUse[0] < 0):
                self.velo[0] -= max((directionUse[0] * aggregate[3]),
                                      directionUse[0] * (vmag(self.velo) - aggregate[1]))
            else:
                self.velo[0] -= min((directionUse[0] * aggregate[3]),
                                      directionUse[0] * (vmag(self.velo) - aggregate[1]))
            if (self.velo[1] < 0):
                self.velo[1] -= max((directionUse[1] * aggregate[3]),
                                      directionUse[1] * (vmag(self.velo) - aggregate[1]))
            else:
                # print(playerSpeed[1], directionUse[1], directionUse[1] * aggregate[3])
                self.velo[1] -= min((directionUse[1] * aggregate[3]),
                                      directionUse[1] * (vmag(self.velo) - aggregate[1]))
                # print(playerSpeed[1])
            if ('slowdamage' in aggregate[4]):
                # print('hey', aggregate[4]['slowdamage'],
                #       aggregate[4]['slowdamage'] * (vmag(playerSpeed) - vmag(preSpeed)) * 100)
                self.health += min(0, aggregate[4]['slowdamage'] * (vmag(self.velo) - vmag(preSpeed)) * 10)
            # print('decel done at', playerSpeed)

        if('angle' in aggregate[4]):
            #print(aggregate[4]['angle'])
            spd = vmag(self.velo)
            angle = aggregate[4]['angle'] * math.pi / 180
            self.velo = vmult(spd * math.cos(angle), self.velo)
            self.velo[2] = math.sin(angle) * spd

        if(directionInput == [0, 0]):
            return
        if (directionInput[0] != 0 and directionInput[1] != 0):
            directionInput[0], directionInput[1] = math.sqrt(2) / 2 * directionInput[0], math.sqrt(2) / 2 * \
                                                   directionInput[1]
        simulSpeed = self.velo.copy()
        simulSpeed[0] += directionInput[0] * aggregate[2]
        simulSpeed[1] += directionInput[1] * aggregate[2]
        if (vmag(simulSpeed) < aggregate[1]):
            self.velo = simulSpeed.copy()
        elif (vmag(simulSpeed) < vmag(self.velo)):
            self.velo = simulSpeed.copy()
        elif (vmag(self.velo) <= aggregate[1]):
            # print('ooo')
            # print(vmult(aggregate[1], vmult(1 / vmag(simulSpeed), simulSpeed)))
            self.velo = vmult(aggregate[1], vmult(1 / vmag(simulSpeed), simulSpeed))
        else:
            # print('aaa', vmag(playerSpeed), vmag(vmult(1 / vmag(simulSpeed), simulSpeed)), playerSpeed, simulSpeed)
            self.velo = vmult(vmag(self.velo), vmult(1 / vmag(simulSpeed), simulSpeed))
            # print(playerSpeed)

        if abs(self.velo[0]) < .000001:
            self.velo[0] = 0
        if abs(self.velo[1]) < .000001:
            self.velo[1] = 0
        if abs(self.velo[2]) < .000001:
            self.velo[2] = 0

class playerSprite(entitySprite):
    def __init__(self):
        super().__init__()
        self.weapon = 'spear'
        self.weaponImage = pygame.transform.scale(pygame.image.load(self.weapon + '.png'), (tileSize * 2, tileSize * 2))
        self.normImage = pygame.transform.scale(pygame.image.load('sprite.png'), (tileSize * 2, tileSize * 2))
        angle = math.atan2(self.velo[1] * -1, max(.000001, abs(self.velo[0])) * self.velo[0]) / math.pi * 180
        self.image = pygame.transform.rotate(self.normImage, angle)
        self.rect = self.image.get_rect()
        self.trueRect = self.image.get_rect()

    def update(self):
        angle = math.atan2(self.velo[1] * -1, max(.000001, abs(self.velo[0])) * self.velo[0]) / math.pi * 180
        self.image = pygame.transform.rotate(self.normImage, angle)
        self.image.blit(pygame.transform.rotate(self.weaponImage, angle), (0, 0))
        #print(self.health)
        tempDirect = [0, 0]
        if (keyStates[276] or keyStates[97]): tempDirect[0] = -1
        if (keyStates[273] or keyStates[119]): tempDirect[1] = -1
        if (keyStates[275] or keyStates[100]): tempDirect[0] = 1
        if (keyStates[274] or keyStates[115]): tempDirect[1] = 1
        super().accel(tempDirect)
        super().update()
        #print(res[0] / tileSize, self.pos[0] - ((res[0]) / tileSize / 2), len(mapperNow[0]) - res[0] / tileSize)
        #print(len(mapperNow[0]), len(mapperNow), res[0] / tileSize, res)
        currentSpot[0] = bounder(0, self.pos[0] - ((res[0] - 100) / tileSize / 2), len(mapperNow[0]) - ((res[0] - 100) / tileSize) - 1)
        currentSpot[1] = bounder(0, self.pos[1] - ((res[1] - 100) / tileSize / 2), len(mapperNow) - (res[1] - 100) / tileSize)

class enemySprite(entitySprite):
    def __init__(self, route, weapon = 'axe'):
        self.path = route
        self.destination = 0
        self.progressSteps = 0
        super().__init__(100, [route[0][0], route[0][1], 0], weapon)
        self.normImage = pygame.transform.scale(pygame.image.load('enemysprite.png'), (tileSize * 2, tileSize * 2))
        angle = math.atan2(self.velo[1] * -1, max(.000001, abs(self.velo[0])) * self.velo[0]) / math.pi * 180
        self.image = pygame.transform.rotate(self.normImage, angle)
        self.rect = self.image.get_rect()
        self.trueRect = self.image.get_rect()

    def update(self):
        angle = math.atan2(self.velo[1] * -1, max(.000001, abs(self.velo[0])) * self.velo[0]) / math.pi * 180
        self.image = pygame.transform.rotate(self.normImage, angle)
        if(self.weapon):
            self.weaponImage = pygame.transform.scale(pygame.image.load(self.weapon + '.png'),
                                                      (tileSize * 2, tileSize * 2))
            self.image.blit(pygame.transform.rotate(self.weaponImage, angle), (0, 0))

        if(vmag([self.path[self.destination][0] - self.pos[0], self.path[self.destination][1] - self.pos[1]]) < 2):
            #print(self.progressSteps, self.destination, self.path[self.destination], self.pos, vmag([self.path[self.destination][0] - self.pos[0], self.path[self.destination][1] - self.pos[1]]))
            self.progressSteps += 1
            if self.progressSteps >= 60:
                self.progressSteps = 0
                self.destination += 1
                if self.destination >= len(self.path):
                    self.destination = 0
        else:
            self.progressSteps = 0
            tempDirect = [0, 0]
            if(self.path[self.destination][0] > self.pos[0]): tempDirect[0] = 1
            if(self.path[self.destination][0] < self.pos[0]): tempDirect[0] = -1
            if(self.path[self.destination][1] > self.pos[1]): tempDirect[1] = 1
            if(self.path[self.destination][1] < self.pos[1]): tempDirect[1] = -1

            for i in range(0, 2):
                if(tempDirect[i] != 0):
                    #print(i)
                    if self.velo[i] * tempDirect[i] > 0:
                        if (self.path[self.destination][i] - self.velo[i] * 50 - self.pos[i]) * tempDirect[i] < 0:
                            tempDirect[i] = 0
                        if (self.path[self.destination][i] - self.velo[i] * 30 - self.pos[i]) * tempDirect[i] < 0:
                            tempDirect[i] = -1 * tempDirect[i]

            #print(tempDirect)
            self.accel(tempDirect)
        super().update()


def getTile(x, y):
    return(mapperNow[x][y])

player = playerSprite()
spritesGrouper = pygame.sprite.Group(player)
# testEnemy = enemySprite([[10, 10], [10, 20]])
# testEnemy.weapon = 'sword'
# spritesGrouper.add(testEnemy)

def getNew(levelText):
    global mapperNow, subSurf, worldSurf, currentSpot, playerSpot, enemies, helps, items, enweps, res
    newLevel(levelText)
    for i in range(0, len(enemies)):
        spritesGrouper.add(enemySprite(enemies[i], enweps[i]))
    res = list(dispsurf.get_size())
    player.health = 100
    player.velo = [0, 0, 0]
    player.pos = [10, 10, 0]
healthSurf = pygame.image.load('hud/hp.png')
needleSurf = pygame.image.load('hud/needle.png')

levelSpot = 0

def playerAttack():
    if not player.weapon:
        return
    fakeSprt = copy.copy(player)
    fakeSprt.radius = weaponStats[player.weapon][0] * tileSize
    enemiesHit = pygame.sprite.spritecollide(fakeSprt, spritesGrouper, False, pygame.sprite.collide_circle)
    for i in range(1, len(enemiesHit)):
        #print('hey!', i, enemiesHit[i].health)
        if(enemiesHit[i].damageCool == 0):
            enemiesHit[i].health -= weaponStats[player.weapon][1]
            enemiesHit[i].damageCool = 60
        if enemiesHit[i].health <= 0:
            enemiesHit[i].kill()
playerAttacks = 0


while(True):
    if(len(spritesGrouper.sprites())) == 1 and levelSpot < len(levels):
        getNew(levels[levelSpot])
        levelSpot += 1
        #res = list(dispsurf.get_size())
        #print('hey')
    player.health = min(100, player.health + 1 / 60)
    if(player.health < 0):
        print('you lose')
        pygame.quit()
        sys.exit()
    if(playerAttacks > 0):
        playerAttack()
        playerAttacks -= 1
        if(playerAttacks == 0):
            player.attackCool = weaponStats[player.weapon][1]
    spriteList = spritesGrouper.sprites()
    for i in range(0, len(spriteList)):
        if spriteList[i] == player:
            continue
        if spriteList[i].weapon:
            if spriteList[i].attackCool == 0:
                if player.damageCool == 0:
                    temper = copy.copy(spriteList[i])
                    temper.radius = weaponStats[spriteList[i].weapon][0] * tileSize
                    if(not pygame.sprite.collide_circle(player, temper)):
                        continue
                    player.health -= weaponStats[spriteList[i].weapon][1] / 4
                    spriteList[i].attackCool = weaponStats[spriteList[i].weapon][2]
                    player.damageCool = 30

    #player.health -= .25
    #res = list(pygame.display.get_window_size())
    # res[0] = res[0] * .9
    # res[1] = res[1] * .9
    #print(player.health)
    #print(tilesOn(player.rect))
    #print(playerSpeed)
    #print(subSurf, worldSurf)
    spritesGrouper.clear(subSurf, worldSurf)
    spritesGrouper.update()
    spritesGrouper.draw(subSurf)
    #dispRes = (int(res[0] / tileSize / 2) * 2, int(res[1] / tileSize / 2) * 2)
    #print(currentSpot, dispRes)
    #playerMove()
    #playerAccel(tempDirect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            #print(event.key)
            if len(keyStates) < event.key:
                for i in range(len(keyStates), event.key + 1):
                    keyStates.append(False)
            keyStates[event.key] = True
            if(event.key == K_SPACE and player.attackCool == 0 and playerAttacks == 0):
                playerAttacks = 30
        if event.type == KEYUP:
            #print(event.key)
            if len(keyStates) < event.key:
                for i in range(len(keyStates), event.key + 1):
                    keyStates.append(False)
            keyStates[event.key] = False
        if event.type == VIDEORESIZE:
            dispsurf = pygame.display.set_mode((max(433, event.size[0]), max(433, event.size[1])), pygame.RESIZABLE)
            #print(event)
            res = list(dispsurf.get_size())
            hudsurf = dispsurf.convert_alpha(dispsurf)
            hudsurf.fill((0, 0, 0, 0))
            hudsurf.blit(surf00, (0, 0))
            hudsurf.blit(surf02, (0, res[1] - 231))
            hudsurf.blit(surf20, (res[0] - 231, 0))
            hudsurf.blit(surf22, (res[0] - 231, res[1] - 231))
            hudsurf.blit(pygame.transform.scale(surf01, (surf01.get_width(), res[1] - 432)), (0, 231))
            hudsurf.blit(pygame.transform.scale(surf10, (res[0] - 432, surf10.get_height())), (231, 0))
            hudsurf.blit(pygame.transform.scale(surf10, (res[0] - 432, surf10.get_height())), (231, res[1] - 50))
            hudsurf.blit(pygame.transform.scale(surf01, (surf01.get_width(), res[1] - 432)), (res[0] - 50, 231))
    #pygame.draw.rect(subSurf, (255, 255, 255), (playerSpot[0] * tileSize, playerSpot[1] * tileSize, tileSize, tileSize))

    blitPos = (currentSpot[0] * tileSize, currentSpot[1] * tileSize)
    dispsurf.blit(subSurf,
                      (50, 50, res[0] - 100, res[1] - 100),
                      (blitPos[0], blitPos[1], res[0] - 100, res[1] - 100))
    dispsurf.blit(hudsurf, (0, 0))
    offsetNow = (100 - player.health) / 100 * healthSurf.get_height()
    #print(offsetNow, player.health)
    dispsurf.blit(healthSurf, (11, 11 + offsetNow), (0, offsetNow, healthSurf.get_width(), healthSurf.get_height() - offsetNow))
    #print(max(.000001, abs(player.velo[0])) * player.velo[0])
    angle = math.atan2(player.velo[1] * -1, max(.000001, abs(player.velo[0])) * player.velo[0] / max(.000001, abs(player.velo[0]))) / math.pi * 180
    #print(angle)
    rotsurf = pygame.transform.rotate(needleSurf, angle)
    dispsurf.blit(rotsurf, (res[0] - 103 - (rotsurf.get_width() - needleSurf.get_width()) / 2, 11 - (rotsurf.get_width() - needleSurf.get_width()) / 2))


    lastPos = playerSpot.copy()
    #print('looped')
    pygame.display.update()
    FPSCLOCK.tick(FPS)