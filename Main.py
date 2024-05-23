#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Function to know if an string could be an integer
def isInt(text):
    try:
        int(text)
    except:
        return False
    else:
        return True
    
#Get locations around a location
def getCloseLocations(loc, radious):
    locs = []
    for x in range(radious*(-1),radious+1):
        for y in range(radious*(-1),radious+1):
            locs.append([loc[0]+x,loc[1]+y])
    return locs

#Sum fo 2dVectors
def sumVectors(vectors):
    finsum = [0,0]
    for i in vectors:
        finsum[0] = finsum[0] + i[0]
        finsum[1] = finsum[1] + i[1]
    return finsum


# In[8]:


def compared(start, end):
    if start < end:
        return 1
    else:
        return -1
    
def shortestWay(a, b):
    c = []
    while a != b:
        for i in range(2):
            if a[i] != b[i]:
                a[i] = a[i] + compared(a[i],b[i])
                c.append(a[:])
    return c

def eleWay(a,b):
    c = []
    for i in range(2):
        while a[i] != b[i]:
            a[i] = a[i] + compared(a[i],b[i])
            c.append(a[:])
    return c

def generateWays(ways):
    del ways[-1]
    for i in ways:
        floor(i)
    return


# In[19]:


#Base class to every object to be printed
class baseObj:
    def __init__(self, location=[0,0], icon = '', activated=True, block=False, floor=False):
        self.icon = icon
        self.location = location
        self.activated = activated
        self.floor = floor
        self.block = block
        if activated == True:
            actors.append(self)
        objects.append(self)
        
    def getLoc(self):
        return self.location
        
    def getX(self):
        return self.location[0]
    
    def getY(self):
        return self.location[1]
    
    def getIcon(self):
        return self.icon
    
    def getActivated(self):
        return self.activated
    
    def activate(self):
        self.activated = True
        actors.append(self)
        return
    
    def blockPlayer(self):
        return self.block
    
    def isFloor(self):
        return self.floor
    
    def interact(self):
        return None
    

    
#Class for the path for the character
class floor(baseObj):
    def __init__(self, location, icon='#', activated=False, block=False, floor=True):
        super().__init__(location, icon, activated, block, floor)
        
        
        
class wall(baseObj):
    def __init__(self, location, icon='*', activated=False, block=True):
        super().__init__(location, icon, activated, block)
        
        
        
class key(baseObj):
    def __init__(self, location, icon='+', activated=False, block=False, floor=True):
        super().__init__(location, icon, activated, block, floor)
        
    def interact(self):
        self.icon = '#'
        player.getKey()
        print('\nYou have gotten an key. It is extremly big and with and sphere at the end of the stick.\n')
        
        
        
class chest(baseObj):
    def __init__(self, location, icon='O', activated=False, block=False, floor=True):
        super().__init__(location, icon, activated, block, floor)
        
    def interact(self):
        global executing
        if player.hasKey() == True:
            self.icon = '#'
            self.block = False
            self.floor = True
            print('\nYou do not have time for god, you just have time to escape. The time is ending and becoming darker. It is about you and the mind of the world.\n')
            executing = False
        else:
            print('\nYou need a KEY to open this big box of dreams and imagination.\n')
             
            
    
#Base class for playable character
class character(baseObj):
    def __init__(self, name, location, icon='@', activated=True):
        super().__init__(location, icon, activated)
        self.name = name
        self.key = False
        floor(self.location)
        
    def getKey(self):
        self.key = True
        return
    
    def hasKey(self):
        return self.key

    def activateCloseObjects(self):
        for i in getCloseLocations(self.location, 20):
            if getObject(i) != None:
                getObject(i).activate()
        return
    
    def move(self, vector=[0,0]):
        nextLoc = sumVectors([self.location, vector])
        nextObj = getObject(nextLoc)
        if nextObj == None:
            print('There is no floor, it is just empty.')
            
        else:
            getObject(nextLoc).interact()   
            
            if nextObj.isFloor() == True:
                self.location = nextLoc
                self.activateCloseObjects()                
            
            elif nextObj.blockPlayer() == True:
                print('You cannot pass through this.')


# In[5]:


#Get a list of actors
def getObjectsX(X, actors):
    for i in actors:
        if i.getX() == X:
            return i
    return 0

def getObject(loc, classname=''):
    for i in objects:
        if i.getX() == loc[0] and i.getY() == loc[1]:
            if classname != '':
                if type(i).__name__ == classname:
                    return i
            else:
                return i
    return None


#Get all character of a coordinate Y
def stringLine(lineY):
    lineA = list(filter(lambda x: x.getY() == lineY, actors))
    line = '|'
    for n in range(XSize):
        actorX = getObjectsX(n, lineA)
        if actorX != 0:
            line += actorX.getIcon()
        else:
            line += ' '
    line += '|'
    return line


#Print all the Y lines with screen borders
def printScreen():
    print('_'*(XSize+2))
    for i in range(YSize):
        print(stringLine(i))
    print('|', '_'*(XSize-2), '|')  
    return


# In[20]:


actors = []
objects = []
seed = 0
XSize = 20
YSize = 5


player = character(input('What is your name? '), [0,0])

chest([4,0])
generateWays(shortestWay([4,0], player.getLoc()))
key([5,4])
generateWays(eleWay([5,4], player.getLoc()))

player.activateCloseObjects()


executing = True

while executing == True:
    printScreen()
    match input().lower():
        
        case 'stop':
            executing = False
        
        case 'up':
            player.move([0,-1])
        case 'down':
            player.move([0,1])
        case 'right':
            player.move([1,0])
        case 'left':
            player.move([-1,0])
        case 'stats':
            player.printStats()

