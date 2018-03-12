from __future__ import print_function
from __future__ import division
from random import randint
from collections import defaultdict
from copy import deepcopy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.axes3d import get_test_data
from matplotlib import cm
import numpy as np
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
a time-varying scalar step-size of at = 1/N(st, at) and an -greedy exploration
strategy with t = N0/(N0 + N(st)), where N0 = 100 is a constant, N(s) is
the number of times that state s has been visited, and N(s, a) is the number
of times that action a has been selected from state s. Feel free to choose an
alternative value for N0, if it helps producing better results. Plot the optimal
value function V*(s) = max_a(Q*(s, a)) using similar axes to the following figure
taken from Sutton and Barto's Blackjack example.  
'''
class MonteCarloAgent():
        

    def __init__(self):
        self.value_fn=[[0 for i in range (11)] for i in range(22)]
        # 2 set of actions for each card you have for each card the dealer has
        self.state_action_counter=[[[0 for i in range (11)] for i in range(22)] for i in range(2)]

        self.state_visit_counter=[[0 for i in range (11)] for i in range(22)]
        self.n=0
        self.states=[]
        self.actions=[]
        self.n_zero = 100
    def run_test(self):
        self.calc_step_test()
        self.update_policy_test()

    def calc_step(self, state,action):
        return 1/self.state_action_counter[action][state[1]][state[0]]

    def calc_step_test(self):
        self.state_action_counter[STICK][15][2]=2
        action=STICK
        state=[2,15]
        result=self.calc_step(state,action)
        assert(result==.5)
        self.state_action_counter[STICK][15][2]=0

    def find_next_action(self,state):
        action=self.monte_carlo_policy(state)
        self.update_count(deepcopy(state),action)
        self.states.append(deepcopy(state))
        self.actions.append(action)
        return action

    def update_count(self,state,action):
        self.state_action_counter[action][state[1]][state[0]]+=1
        self.state_visit_counter[state[1]][state[0]]+=1

    def update_policy(self,reward,state):
        # if state[1]<=21 and state[1]>0:
        #     self.states.append(deepcopy(state))
        #     self.actions.append(WAIT)
        #     self.update_count(deepcopy(state),action)
        for i in range(len(self.actions)):
            action=self.actions[i]
            state=self.states[i]
            state_count=self.state_visit_counter[state[1]][state[0]]
            state_action_count=self.state_action_counter[action][state[1]][state[0]]
            value_count=self.value_fn[state[1]][state[0]]
            self.value_fn[state[1]][state[0]]=value_count+self.calc_step(state,action)*(reward-value_count)
        self.actions=[]
        self.states=[]

    def update_policy_test(self):
        self.states=[[2,8],[2,8],[2,16]]
        self.actions=[STICK,STICK,WAIT]
        reward=1
        self.state_visit_counter[8][2]+=1
        self.state_action_counter[STICK][8][2]+=1
        self.state_visit_counter[8][2]+=1
        self.state_action_counter[STICK][8][2]+=1
        self.state_visit_counter[16][2]+=1
        self.state_action_counter[WAIT][16][2]+=1
        self.update_policy(reward,[24,16])
        self.states=[[2,8],[2,8],[2,16]]
        self.actions=[STICK,STICK,WAIT]
        assert(self.value_fn[8][2]==.75)
        assert(self.value_fn[16][2]==1)
        reward=0
        self.state_visit_counter[8][2]+=1
        self.state_action_counter[STICK][8][2]+=1
        self.state_visit_counter[8][2]+=1
        self.state_action_counter[STICK][8][2]+=1
        self.state_visit_counter[16][2]+=1
        self.state_action_counter[WAIT][16][2]+=1
        self.update_policy(reward,[24,16])
        print(self.value_fn[8][2])
        assert(self.value_fn[8][2]==.421875)
        print(self.value_fn[16][2])
        assert(self.value_fn[16][2]==.5)
        
    def monte_carlo_policy(self,state):
        hit_chance=self.n_zero/(self.n_zero+self.state_visit_counter[state[1]][state[0]])
        if randint(0,100) < hit_chance*100:
            return STICK
        else:
            return WAIT


    def __str__(self):
        for i in range(len(self.value_fn)):
            print("Player has a ",i)
            for j in range(len(self.value_fn[i])):
                print("{:+.1f}".format(self.value_fn[i][j]),end =" ")
            print()    
        # for i in range(len(self.value_fn)):
        #     for j in range(len(self.value_fn[i])):
        #         print("%2d" % self.state_visit_counter[i][j],end =" ")
        #     print()
        # for i in range(len(self.value_fn)):
        #     for j in range(len(self.value_fn[i])):
        #         print("%2d" % self.state_visit_counter[i][j],end =" ")
        #     print()    
        return "Contents of the Agent"




plt.show()
TEST=False
agent=MonteCarloAgent()
if TEST==False:
    state = setupenviroment()
    states=[]
    actions=[]
    for i in range(1000000):
        action=agent.find_next_action(state)
        state, reward, done=step(state,action)
        if done==True:
            agent.update_policy(reward,state)
            states=[]
            action=[]
            state = setupenviroment()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    arr=np.array(agent.value_fn)
    X, Y, Z = get_test_data(0.05)
    X_2=np.array([i for i in range (11)])
    Y_2=np.array([i for i in range (22)])
    X_2, Y_2 = np.meshgrid(X_2, Y_2)
    Z_2=np.array(agent.value_fn)
    ax.plot_wireframe(X_2, Y_2, Z_2)
    ax.set_xlabel('Dealer`s Hand')
    ax.set_ylabel('Your Hand')
    ax.set_zlabel('Reward')
    plt.show()
else:
    agent.run_test()
