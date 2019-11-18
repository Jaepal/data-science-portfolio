import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import slot

slots = ['Platinum', 'Monster']
N_experiments = 100
N_episodes = 10000
epsilon = 0.1
rtp_values = np.array([0.583, 0.416])

class Bandit:
    
    def __init__(self, bpl, slots):
        self.N = len(slots) # bandit(slot machine)의 숫자
        self.bpl = bpl
        self.slot_platinum = slot.game_platinum(bpl)
        self.slot_monster = slot.game_monster(bpl)
    
    def spin_slot(self, i):
        if i == 0:
            return self.slot_platinum.play_platinum()
        elif i == 1:
            return self.slot_monster.play_monster()

class EpsilonGreedy:
    
    def __init__(self, bandit, epsilon):
        self.epsilon = epsilon
        self.k = np.zeros(bandit.N, dtype=np.int)
        self.Q = np.zeros(bandit.N, dtype=np.float)
    
    def get_action(self, bandit):
        rand = np.random.random()
        if rand < self.epsilon:
            action_explore = np.random.randint(bandit.N)
            return action_explore
        else:
            action_greedy = np.random.choice(np.flatnonzero(self.Q == self.Q.max()))
            return action_greedy
        
    def update_Q(self, action, reward):
        self.k[action] += 1
        self.Q[action] += (1./self.k[action]) * (reward - self.Q[action])

class UCB:
    
    def __init__(self, bandit):
        self.k = np.zeros(bandit.N, dtype=np.int)
        self.Q = np.zeros(bandit.N, dtype=np.float)

    def get_action(self, bandit):
        for arm in range(bandit.N):
          if self.k[arm] == 0:
            return arm
        
        ucb_values = [0.0 for arm in range(bandit.N)]
        total_counts = sum(self.k)
        for arm in range(bandit.N):
            ucb_values[arm]= self.Q[arm] / self.k[arm] + (2 * np.log(total_counts) / self.k[arm]) ** 0.5
        return np.argmax(ucb_values)
    
    def update_Q(self, action, reward):
        self.k[action] += 1
        self.Q[action] += (1./self.k[action]) * (reward - self.Q[action])

class TS:
    
    def __init__(self, bandit):
        self.k = np.zeros(bandit.N, dtype=np.int)
        self.Q = np.zeros(bandit.N, dtype=np.float)
        self.theta = np.zeros(bandit.N, dtype=np.int)
        self.alpha = np.ones(bandit.N, dtype=np.float)
        self.beta = np.ones(bandit.N, dtype=np.float)
        self.prior_distributions = [stats.beta(a=self.alpha[i], b=self.beta[i]) for i in range(bandit.N)]
        self.S = 100000000
    
    def get_action(self, bandit):
        theta_samples = [float(dist.rvs(1)) for dist in self.prior_distributions]
        return np.argmax(theta_samples)
    
    def update_Q(self, action, reward):
        while(reward >= 60000):
            self.k[action] += 1
            self.Q[action] += (1./self.k[action]) * (60000 - self.Q[action])
            self.beta[action] += 1
            reward -= 60000
        self.k[action] += 1
        self.Q[action] += (1./self.k[action]) * (reward - self.Q[action])
        self.alpha[action] += 1 - reward / 60000
        self.beta[action] += reward / 60000
        self.prior_distributions[action] = stats.beta(a=self.alpha[action], b=self.beta[action])

def cal_regret(rtp_values, choices):
    w_opt = rtp_values.max()
    return (w_opt - rtp_values[choices.astype(int)]).cumsum()

def experiment(agent, bandit, N_episodes):
    action_history = []
    reward_history = []
    regret_history = []
    for episode in range(N_episodes):
        action = agent.get_action(bandit)
        reward = bandit.spin_slot(action)
        regret = cal_regret(rtp_values, action)
        agent.update_Q(action, reward)
        action_history.append(action)
        reward_history.append(reward)
        regret_history.append(regret)
        
    return action_history, reward_history, regret_history


N_bandits = len(slots)
print("Running multi-armed bandits with N_bandits = {} and agent epsilon = {}".format(N_bandits, epsilon))
reward_history_avg = np.zeros(N_episodes)  # reward history experiment-averaged
action_history_sum = np.zeros((N_episodes, N_bandits))  # sum action history

for i in range(N_experiments):
    print('Exp', i)
    """
    bandit = Bandit(2000, slots)
    #agent = EpsilonGreedy(bandit, epsilon)
    agent = TS(bandit)
    """
    bandit = Bandit(2000, slots)
    agent = TS(bandit)
    (action_history, reward_history, regert_history) = experiment(agent, bandit, N_episodes)
    
    #if (i + 1)% (N_experiments / 100) == 0:
    print("[Experiment {}/{}], N_episodes = {}".format(i + 1, N_experiments, N_episodes))
    print("  average reward = {}".format(np.sum(reward_history) / len(reward_history)))
    print("")
    # Sum up experiment reward (later to be divided to represent an average)
    reward_history_avg += reward_history
    # Sum up action history
    for j, (a) in enumerate(action_history):
        action_history_sum[j][a] += 1

reward_history_avg /= np.float(N_experiments)
print("reward history avg = {}".format(reward_history_avg))


"""
plt.plot(reward_history_avg)
plt.xlabel("Episode number")
plt.ylabel("Rewards collected".format(N_experiments))
plt.title("Bandit reward history averaged over {} experiments (epsilon = {})".format(N_experiments, epsilon))
ax = plt.gca()
ax.set_xscale("log", nonposx='clip')
plt.xlim([1, N_episodes])
plt.show()
"""
agent.alpha
agent.beta
plt.figure(figsize=(18, 12))
for i in range(N_bandits):
    action_history_sum_plot = 100 * action_history_sum[:,i] / N_experiments
    plt.plot(list(np.array(range(len(action_history_sum_plot)))+1),
             action_history_sum_plot,
             linewidth=5.0,
             label="Bandit #{}".format(i+1))
plt.title("Bandit action history averaged over {} experiments (epsilon = {})".format(N_experiments, epsilon), fontsize=26)
plt.xlabel("Episode Number", fontsize=26)
plt.ylabel("Bandit Action Choices (%)", fontsize=26)
leg = plt.legend(loc='upper left', shadow=True, fontsize=26)
ax = plt.gca()
ax.set_xscale("log", nonposx='clip')
plt.xlim([1, N_episodes])
plt.ylim([0, 100])
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)
for legobj in leg.legendHandles:
    legobj.set_linewidth(16.0)
plt.show()

agent.alpha
agent.beta

regert_history