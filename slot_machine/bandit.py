import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class eps_bandit:
    '''
    epsilon-greedy 알고리즘
    
    Inputs
    =================
    k : number of arms(int)
    eps: probability of random action 0 < eps < 1 (float)
    iters: number of steps (int)
    '''
    def __init__(self, k, eps, iters):
        # Number of arms
        self.k = k
        # Search probability
        self.eps = eps
        # Step count
        self.iters = iters
        # Step count for each arm
        self.k_n = np.zeros(k)
        # Total mean reward
        self.mean_reward = 0
        self.reward = np.zeros(iters)
        # Mean reward for each arm
        self.k_reward = np.zeros(k)
    
    def pull(self):
        p = np.random.rand()
        if self.eps == 0 and self.n == 0:
            a = np.random.choice(self.k)
        elif p < self.eps:
            # Randomly select an action
            a = np.random.choice(self.k)
        else:
            # Take greedy action
            a = np.argmax(self.k_reward)
        
        reward = np.random.normal(self.mu[a], 1)