import pandas as pd
import numpy as np

class game_platinum:
    """
    platinum 슬롯 구현
    """
    
    def __init__(self, bpl):
        self.bpl = bpl
        self.paylines = [[1, 4, 7, 10, 13],
                         [0, 3, 6, 9, 12],
                         [2, 5, 8, 11, 14],
                         [0, 4, 8, 10, 12],
                         [2, 4, 6, 10, 14],
                         [0, 3, 7, 11, 14],
                         [2, 5, 7, 9, 12],
                         [1, 5, 8, 11, 13],
                         [1, 3, 6, 9, 13],
                         [0, 4, 7, 10, 12],
                         [2, 4, 7, 10, 14],
                         [0, 4, 6, 10, 12],
                         [2, 4, 8, 10, 14],
                         [1, 4, 6, 10, 13],
                         [1, 4, 8, 10, 13],
                         [1, 5, 7, 9, 13],
                         [1, 3, 7, 11, 13],
                         [0, 5, 6, 11, 12],
                         [2, 3, 8, 9, 14],
                         [1, 3, 8, 9, 13],
                         [1, 5, 6, 11, 13],
                         [0, 3, 8, 9, 12],
                         [2, 5, 6, 11, 14],
                         [0, 5, 8, 11, 12],
                         [2, 3, 6, 9, 14],
                         [0, 3, 7, 9, 12],
                         [2, 5, 7, 11, 14],
                         [0, 4, 8, 11, 14],
                         [2, 4, 6, 9, 12],
                         [1, 3, 7, 9, 13]]
        self.rich_reward_list = [0, 0, 0, 30, 90, 240, 900, 2250, 15000, 30000]
        self.pl_labels = ['Q', '10', 'K', 'A', 'J', 'Ca', 'Cr', 'D', 'Co', 'W', 'R']
        self.col_types = ['3', '2-1', '2-2', '2-3', '1']
        self.pl_paytable = pd.read_csv('../data/slot_machine/platinum_csv/pl_paytable.csv')
        self.pl_all = pd.read_csv('../data/slot_machine/platinum_csv/pl_all.csv')

    def get_platinum_coltype(self, i):
        if i==0:
            return np.random.choice(self.col_types, 1, p=[0.545, 0.21, 0.09, 0.085, 0.07]).tolist()[0]
        if i==1:
            return np.random.choice(self.col_types, 1, p=[0.44, 0.195, 0.055, 0.225, 0.085]).tolist()[0]
        if i==2:
            return np.random.choice(self.col_types, 1, p=[0.465, 0.16, 0.06, 0.195, 0.12]).tolist()[0]
        if i==3:
            return np.random.choice(self.col_types, 1, p=[0.55, 0.10, 0.095, 0.215, 0.04]).tolist()[0]
        if i==4:
            return np.random.choice(self.col_types, 1, p=[0.39, 0.245, 0.035, 0.085, 0.245]).tolist()[0]

    def get_platinum_symbol(self, col_type, probs, r_full=0):
        if r_full:
            n_labels = self.pl_labels[:10]
            n_probs = [i / sum(probs[:10]) for i in probs[:10]]
        else:
            n_labels = self.pl_labels
            n_probs = [i / sum(probs) for i in probs]
        if col_type == '3':
            reel = np.random.choice(n_labels, 3, replace=False, p=n_probs).tolist()
        elif col_type == '2-1':
            reel = np.random.choice(n_labels, 2, replace=False, p=n_probs).tolist()
            reel.insert(1, reel[0])
        elif col_type == '2-2':
            reel = np.random.choice(n_labels, 2, replace=False, p=n_probs).tolist()
            reel.insert(2, reel[0])
        elif col_type == '2-3':
            reel = np.random.choice(n_labels, 2, replace=False, p=n_probs).tolist()
            reel.reverse()
            reel.insert(2, reel[1])
        elif col_type == '1':
            reel = np.random.choice(n_labels, 1, replace=False, p=n_probs).tolist() * 3
        return reel

    def get_weighted_probability(self, game):
        weight = [25, 19, 27, 24, 23, 19, 15, 16, 18, 6, 8]
        switch = [1] * 11
        game_copy = game.copy()
        reel_list = []
        tmp = []
        count = [0] * 11
        itr = 0
        while(len(game_copy) >= 3):
            for i in range(3):
                tmp.append(game_copy.pop(0))
            reel_list.append(tmp)
            for n, s in enumerate(self.pl_labels):
                
                if s in reel_list[itr]:
                    count[n] += 1
                
                if s in tmp and s != 'R':
                    switch[n] *= 1.4
                
            tmp = []
            itr += 1
        for i in range(len(count)-1):
            if count[i] == 2:
                switch[i] *= 4.5
            elif count[i] == 3:
                switch[i] *= 3.5
            elif count[i] == 4:
                switch[i] *= 5
            else:
                continue
        probs = [w*(switch[n]) for n, w in enumerate(weight)]
        return probs    
    
    def spin_platinum(self):
        game = []
        r_full = 0
        for i in range(5):
            probs = self.get_weighted_probability(game)
            if game.count('R') >= 7:
                r_full = 1
            col_type = self.get_platinum_coltype(i)
            game.extend(self.get_platinum_symbol(col_type, probs, r_full))
        return game

    def get_platinum_payline_symbol(self, lst):
        if len(set(lst)) < 2:
            return lst[0]
        else:
            for x in list(set(lst)):
                if x != 'W':
                    return x
                else:
                    continue

    def check_rich(self, game):
        rnum = game.count('R')
        return self.bpl * self.rich_reward_list[rnum]

    def cal_platinum_payline(self, game):
        pay = 0
        pay_type_list = []
        
        # RICH 보너스 계산
        pay += self.check_rich(game)
        
        # payline 계산
        for payline in self.paylines:
            tmp = []
            for i in range(5):
                if i == 4:
                    tmp.append(game[payline[i]])
                    break
                if i == 0 and game[payline[i]] == 'W':
                    tmp.append(game[payline[i]])
                elif game[payline[i]] != game[payline[i+1]] and game[payline[i+1]] != 'W':
                    if game[payline[i+1]] in tmp:
                        tmp.append(game[payline[i]])
                    else:
                        tmp.append(game[payline[i]])
                        break
                else:
                    tmp.append(game[payline[i]])
            if len(tmp) >= 3:
                sym = self.get_platinum_payline_symbol(tmp)
                pay += self.pl_paytable.loc[len(tmp)-3, sym] * self.bpl
                pay_type_list.append(tmp)
        return pay, pay_type_list


    def play(self):
        
        game = self.spin_platinum()
        pay = self.cal_platinum_payline(game)[0]
        return pay

class game_monster:
    """
    monster 슬롯 구현
    """
    
    def __init__(self, bpl):
        self.bpl = bpl
        self.paylines = [[1, 4, 7, 10, 13],
                         [0, 3, 6, 9, 12],
                         [2, 5, 8, 11, 14],
                         [0, 4, 8, 10, 12],
                         [2, 4, 6, 10, 14],
                         [0, 3, 7, 11, 14],
                         [2, 5, 7, 9, 12],
                         [1, 5, 8, 11, 13],
                         [1, 3, 6, 9, 13],
                         [0, 4, 7, 10, 12],
                         [2, 4, 7, 10, 14],
                         [0, 4, 6, 10, 12],
                         [2, 4, 8, 10, 14],
                         [1, 4, 6, 10, 13],
                         [1, 4, 8, 10, 13],
                         [1, 5, 7, 9, 13],
                         [1, 3, 7, 11, 13],
                         [0, 5, 6, 11, 12],
                         [2, 3, 8, 9, 14],
                         [1, 3, 8, 9, 13],
                         [1, 5, 6, 11, 13],
                         [0, 3, 8, 9, 12],
                         [2, 5, 6, 11, 14],
                         [0, 5, 8, 11, 12],
                         [2, 3, 6, 9, 14],
                         [0, 3, 7, 9, 12],
                         [2, 5, 7, 11, 14],
                         [0, 4, 8, 11, 14],
                         [2, 4, 6, 9, 12],
                         [1, 3, 7, 9, 13]]
        self.ms_labels = ['10', 'J', 'Q', 'K', 'A', 'GGM', 'OM', 'RM', 'GWM', 'W', 'S']
        self.ms_paytable = pd.read_csv('../data/slot_machine/monster_csv/ms_paytable.csv')
        self.ms_all = pd.read_csv('../data/slot_machine/monster_csv/ms_all.csv')
        self.col_types = ['3', '2-1', '2-2', '2-3', '1']
    
    def get_monster_coltypes(self, i):
        if i==0:
            return np.random.choice(self.col_types, 1, p=[0.496, 0.109, 0.021, 0.1, 0.274]).tolist()[0]
        if i==1:
            return np.random.choice(self.col_types, 1, p=[0.364, 0.11, 0.03, 0.127, 0.369]).tolist()[0]
        if i==2:
            return np.random.choice(self.col_types, 1, p=[0.517, 0.09, 0.021, 0.1, 0.272]).tolist()[0]
        if i==3:
            return np.random.choice(self.col_types, 1, p=[0.33, 0.125, 0.043, 0.119, 0.383]).tolist()[0]
        if i==4:
            return np.random.choice(self.col_types, 1, p=[0.466, 0.076, 0.013, 0.089, 0.356]).tolist()[0]

    def get_monster_scatter(self):
        return np.random.choice([0, 1, 2, 3], 1, p=[0.4325, 0.431, 0.1225, 0.014]).tolist()[0]

    def get_monster_symbol(self, col_type, probs):
        n_labels = self.ms_labels[:10]
        n_probs = [i / sum(probs) for i in probs]

        if col_type == '3':
            reel = np.random.choice(n_labels, 3, replace=False, p=n_probs).tolist()
        elif col_type == '2-1':
            reel = np.random.choice(n_labels, 2, replace=False, p=n_probs).tolist()
            reel.insert(1, reel[0])
        elif col_type == '2-2':
            reel = np.random.choice(n_labels, 2, replace=False, p=n_probs).tolist()
            reel.insert(2, reel[0])
        elif col_type == '2-3':
            reel = np.random.choice(n_labels, 2, replace=False, p=n_probs).tolist()
            reel.reverse()
            reel.insert(2, reel[1])
        elif col_type == '1':
            reel = np.random.choice(n_labels, 1, replace=False, p=n_probs).tolist() * 3
        return reel
    
    def get_monster_weighted_probability(self, game):
        weight = [26, 24, 28, 28, 25, 19, 15, 13, 9, 3]
        switch = [1] * 10
        game_copy = game.copy()
        reel_list = []
        tmp = []
        count = [0] * 11
        itr = 0
        while(len(game_copy) >= 3):
            for i in range(3):
                tmp.append(game_copy.pop(0))
            reel_list.append(tmp)
            for n, s in enumerate(self.ms_labels):
                
                if s in reel_list[itr]:
                    count[n] += 1
                
                if s in tmp and s != 'S':
                    switch[n] *= 1.35
                
            tmp = []
            itr += 1
        for i in range(len(count)-1):
            if count[i] == 2:
                switch[i] *= 4
            elif count[i] == 3:
                switch[i] *= 3
            elif count[i] == 4:
                switch[i] *= 4.5
            else:
                continue
        probs = [w*(switch[n]) for n, w in enumerate(weight)]
        return probs 
    
    def spin_monster(self):
        game = []
        scatter_num = self.get_monster_scatter()
        scatter_position = np.random.choice([0, 2, 4], scatter_num, replace=False, p=[0.434, 0.313, 0.253]).tolist()
        
        for i in range(5):
            probs = self.get_monster_weighted_probability(game)
            col_type = self.get_monster_coltypes(i)
            game.extend(self.get_monster_symbol(col_type, probs))
        for sp in scatter_position:
            game[np.random.randint(sp*3, sp*3+3)] = 'S'
    
        return game
    
    def get_monster_playine_symbol(self, lst):
        if len(set(lst)) < 2:
            return lst[0]
        else:
            for x in list(set(lst)):
                if x != 'W':
                    return x
                else:
                    continue
        
    def cal_monster_payline(self, game):
        pay = 0
        pay_type_list = []
        for payline in self.paylines:
            tmp = []
            for i in range(5):
                if i == 4:
                    tmp.append(game[payline[i]])
                    break
                if i == 0 and game[payline[i]] == 'W':
                    tmp.append(game[payline[i]])
                elif game[payline[i]] != game[payline[i+1]] and game[payline[i+1]] != 'W':
                    if game[payline[i+1]] in tmp:
                        tmp.append(game[payline[i]])
                    else:
                        tmp.append(game[payline[i]])
                        break
                else:
                    tmp.append(game[payline[i]])
            if len(tmp) >= 3:
                sym = self.get_monster_playine_symbol(tmp)
                pay += self.ms_paytable.loc[len(tmp)-3, sym] * self.bpl
                pay_type_list.append(tmp)
        return pay, pay_type_list

    def play(self):
        
        game = self.spin_monster()
        pay = self.cal_monster_payline(game)[0]
        return pay


class game_masque:
    """
    monster 슬롯 구현
    """
    
    def __init__(self, bpl):
        self.bpl = bpl // 3
        self.paylines = [[0, 3, 6, 9, 12],
                         [1, 4, 7, 10, 13],
                         [2, 5, 8, 11, 14],
                         [0, 4, 8, 10, 12],
                         [2, 4, 6, 10, 14],
                         [0, 3, 7, 11, 14],
                         [2, 5, 7, 9, 12],
                         [0, 4, 7, 10, 12],
                         [1, 5, 8, 11, 13],
                         [1, 3, 6, 9, 13],
                         [2, 4, 7, 10, 14],
                         [0, 4, 6, 10, 12],
                         [1, 5, 7, 11, 13],
                         [1, 3, 7, 9, 13],
                         [2, 4, 8, 10, 14],
                         [1, 4, 6, 10, 13],
                         [1, 4, 8, 10, 13],
                         [0, 5, 6, 11, 12],
                         [2, 3, 8, 9, 14],
                         [0, 3, 8, 9, 12],
                         [2, 5, 6, 11, 14],
                         [0, 5, 7, 9, 14],
                         [2, 3, 7, 11, 12],
                         [0, 5, 8, 11, 12],
                         [2, 3, 6, 9, 14],
                         [1, 3, 8, 10, 12],
                         [1, 5, 6, 10, 14],
                         [0, 3, 7, 9, 12],
                         [2, 5, 7, 11, 14],
                         [0, 5, 7, 11, 12]]
        self.mq_labels = ['J', 'Q', 'K', 'A', 'F', 'H', 'Ms', 'St', 'Mn', 'Wm', 'W', 'Sc']
        self.mq_paytable = pd.read_csv('../data/slot_machine/masque_csv/mq_paytable.csv')
        self.mq_all = pd.read_csv('../data/slot_machine/masque_csv/mq_all.csv')
        self.col_types = ['3', '2-1', '2-2', '2-3', '1']

    def get_masque_coltypes(self, i):
        if i==0:
            return np.random.choice(self.col_types, 1, p=[0.596, 0.064, 0.052, 0.069, 0.219]).tolist()[0]
        if i==1:
            return np.random.choice(self.col_types, 1, p=[0.485, 0.154, 0.038, 0.16, 0.163]).tolist()[0]
        if i==2:
            return np.random.choice(self.col_types, 1, p=[0.461, 0.162, 0.076, 0.157, 0.144]).tolist()[0]
        if i==3:
            return np.random.choice(self.col_types, 1, p=[0.51, 0.141, 0.062, 0.132, 0.155]).tolist()[0]
        if i==4:
            return np.random.choice(self.col_types, 1, p=[0.693, 0.084, 0.085, 0.09, 0.048]).tolist()[0]
        
    def get_masque_scatter(self):
        return np.random.choice([0, 1, 2, 3, 4, 5], 1, p=[0.5483, 0.3295, 0.103, 0.017, 0.002, 0.0002]).tolist()[0]
    
    def get_masque_symbol(self, col_type, probs):
        n_labels = self.mq_labels[:11]
        n_probs = [i / sum(probs) for i in probs]

        if col_type == '3':
            reel = np.random.choice(n_labels, 3, replace=False, p=n_probs).tolist()
        elif col_type == '2-1':
            reel = np.random.choice(n_labels, 2, replace=False, p=n_probs).tolist()
            reel.insert(1, reel[0])
        elif col_type == '2-2':
            reel = np.random.choice(n_labels, 2, replace=False, p=n_probs).tolist()
            reel.insert(2, reel[0])
        elif col_type == '2-3':
            reel = np.random.choice(n_labels, 2, replace=False, p=n_probs).tolist()
            reel.reverse()
            reel.insert(2, reel[1])
        elif col_type == '1':
            reel = np.random.choice(n_labels, 1, replace=False, p=n_probs).tolist() * 3
        return reel
    
    def get_masque_weighted_probability(self, game):
        weight = [27, 24, 26, 24, 21, 18, 17, 15, 8, 9, 3]
        switch = [1] * 11
        game_copy = game.copy()
        reel_list = []
        tmp = []
        count = [0] * 11
        itr = 0
        while(len(game_copy) >= 3):
            for i in range(3):
                tmp.append(game_copy.pop(0))
            reel_list.append(tmp)
            for n, s in enumerate(self.mq_labels):
                
                if s in reel_list[itr]:
                    count[n] += 1
                
                if s in tmp and s != 'S':
                    switch[n] *= 1.3
                
            tmp = []
            itr += 1
        for i in range(len(count)-1):
            if count[i] == 2:
                switch[i] *= 4
            elif count[i] == 3:
                switch[i] *= 3
            elif count[i] == 4:
                switch[i] *= 4.5
            else:
                continue
        probs = [w*(switch[n]) for n, w in enumerate(weight)]
        return probs 
    
    def spin_masque(self):
        game = []
        scatter_num = self.get_masque_scatter()
        scatter_position = np.random.choice([0, 1, 2, 3, 4], scatter_num, replace=False, p=[0.185, 0.171, 0.194, 0.234, 0.216]).tolist()
        for i in range(5):
            probs = self.get_masque_weighted_probability(game)
            col_type = self.get_masque_coltypes(i)
            game.extend(self.get_masque_symbol(col_type, probs))
        for sp in scatter_position:
            game[np.random.randint(sp*3, sp*3+3)] = 'Sc'
        
        return game

    def get_symbol(self, lst):
        if len(set(lst)) < 2:
            return lst[0]
        else:
            for x in list(set(lst)):
                if x != 'W':
                    return x
                else:
                    continue
    
    def cal_masque_payline(self, game):
        pay = 0
        pay_type_list = []
        
        for payline in self.paylines:
            tmp = []
            for i in range(5):
                if i == 4:
                    tmp.append(game[payline[i]])
                    break
                if i == 0 and game[payline[i]] == 'W':
                    tmp.append(game[payline[i]])
                elif game[payline[i]] != game[payline[i+1]] and game[payline[i+1]] != 'W':
                    if game[payline[i+1]] in tmp:
                        tmp.append(game[payline[i]])
                    else:
                        tmp.append(game[payline[i]])
                        break
                else:
                    tmp.append(game[payline[i]])
            if len(tmp) >= 3:
                sym = self.get_symbol(tmp)
                pay += self.mq_paytable.loc[len(tmp)-3, sym] * self.bpl
                pay_type_list.append(tmp)
        return pay, pay_type_list
    
    def play(self):
        
        game = self.spin_masque()
        pay = self.cal_masque_payline(game)[0]
        return pay