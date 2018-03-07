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

def setupenviroment():
    return [getcard(0,True),getcard(0,True)]

def step(state, action):
    reward=0
    done=False
    if action == STICK:
        state[1] = getcard(state[1])
        if state[1] > 21:
            done = True
        if state[1] < 0:
            state[1]=0    
            reward = -1
    if action == WAIT:
        done = True
        while state[0] < 17:
            state[0] = getcard(state[0],True)
        if state[0] < state[1] or state[0] > 21:
            reward = 1    
        elif state[0] > state[1]:
            reward = -1

    return state, reward, done





# state=setupenviroment()
# for i in range(10):
#     x=randint(1,100)
#     if x>33:
#         state, reward, done=step(state,STICK)
#     else:
#         state, reward, done=step(state,WAIT) 
#     print(state,reward,done)
#     if done==True:
#         state = setupenviroment()
'''    
2. Monte-Carlo Control in Easy21
Apply Monte-Carlo control to Easy21. Initialise the value function to zero. Use
a time-varying scalar step-size of αt = 1/N(st, at) and an -greedy exploration
strategy with t = N0/(N0 + N(st)), where N0 = 100 is a constant, N(s) is
the number of times that state s has been visited, and N(s, a) is the number
of times that action a has been selected from state s. Feel free to choose an
alternative value for N0, if it helps producing better results. Plot the optimal
value function V∗(s) = max_a(Q∗(s, a)) using similar axes to the following figure
taken from Sutton and Barto’s Blackjack example.  
'''
class MonteCarloAgent():
    n_zero = 100    

    def __init__(self):
        self.value_fn=[[0 for i in range (21)] for i in range(21)]
        # 2 set of actions for each card you have for each card the dealer has
        self.state_action_count=[[[0 for i in range (21)] for i in range(21)] for i in range(2)]

        self.state_visit_count=[[0 for i in range (21)] for i in range(21)]
        self.n=0

    def calc_step(self, state,action):
        return 1/self.state_action_count[action][state[1]][state[0]]

    def find_next_action(self,state,action,reward,first):
        pass

    def update_count(self,state,action,reward):
        pass

    def update_policy(self,state,action,reward):
        pass

    def monte_carlo_policy(self,state):
        hit_chance=n_zero/(n_zero+state_visit_count[state[1]][state[0]])
        if random.randint(0,100) < hit_chance*100:
            return STICK
        else:
            return WAIT


MonteCarloAgent()
state = setupenviroment()
for i in range(10):
    x=randint(1,100)
    if x>33:
        state, reward, done=step(state,STICK)
    else:
        state, reward, done=step(state,WAIT) 
    print(state,reward,done)
    if done==True:
        state = setupenviroment()