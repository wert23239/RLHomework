from random import randint
RED = -1
BLACK = 1
STICK = 0
WAIT = 1

def getcard(current,first=False):
    num = randint(1, 10)
    color = RED
    cardchance = randint(1, 100)
    if cardchance > 33 or first:
        color = BLACK  
    return current+color*num

def step(state, action):
    reward=0
    done=False
    if action == STICK:
        state[1] = getcard(state[1])
        if state[1] > 21:
            done = True
            reward = -1
    if action == WAIT:
        done = True
        while state[0] < 17:
            state[0] = getcard(state[0],False)
        if state[0] < state[1] or state[0] > 21:
            reward = 1    
        elif state[0] > state[1]:
            reward = -1

    return state, reward, done





state=[getcard(0,True),getcard(0,True)]
for i in range(10):
    x=randint(1,100)
    if x>33:
        state, reward, done=step(state,STICK)
    else:
        state, reward, done=step(state,WAIT) 
    print(state,reward,done)
    if done==True:
        state = [getcard(0,True),getcard(0,True)]
    