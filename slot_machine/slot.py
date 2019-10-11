import pandas as pd
import numpy as np

paylines = [[1, 4, 7, 10, 13],
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

labels = ['Q', '10', 'K', 'A', 'J', 'Ca', 'Cr', 'D', 'Co', 'W', 'R']

payTable = pd.read_csv('../data/slot_machine/platinum_csv/payTable.csv')
pl_all = pd.read_csv('../data/slot_machine/platinum_csv/pl_all.csv')
test_game = []
ttmp = []
for n, x in enumerate(pl_all['classname']):
    ttmp.append(x)
    if (n+1) % 15 == 0:
        test_game.append(ttmp)
        ttmp = []

game = ['Co', 'K', 'D', 'K', 'K', 'K', 'K', 'A', 'Co', 'Q', 'A', 'R', 'Ca', 'Ca', 'Ca']
game = ['W', '10', 'J', 'K', 'D', 'Ca', 'Q', 'W', 'Q', 'Co', '10', 'Q', 'Cr', 'Co', 'R']

def getPlatinumColType(i):
    if i==0:
        j = np.random.randint(1, 201)
        if j <= 109:
            return '3'
        elif j <= 151 and j > 109:
            return '2-1'
        elif j <= 169 and j > 151:
            return '2-2'
        elif j <= 186 and j > 169:
            return '2-3'
        elif j > 186:
            return '1'
    if i==1:
        j = np.random.randint(1, 201)
        if j <= 88:
            return '3'
        elif j <= 127 and j > 88:
            return '2-1'
        elif j <= 138 and j > 127:
            return '2-2'
        elif j <= 183 and j > 138:
            return '2-3'
        elif j > 183:
            return '1'
    if i==2:
        j = np.random.randint(1, 201)
        if j <= 93:
            return '3'
        elif j <= 125 and j > 93:
            return '2-1'
        elif j <= 137 and j > 125:
            return '2-2'
        elif j <= 176 and j > 137:
            return '2-3'
        elif j > 176:
            return '1'
    if i==3:
        j = np.random.randint(1, 201)
        if j <= 110:
            return '3'
        elif j <= 130 and j > 110:
            return '2-1'
        elif j <= 149 and j > 130:
            return '2-2'
        elif j <= 192 and j > 149:
            return '2-3'
        elif j > 192:
            return '1'
    if i==4:
        j = np.random.randint(1, 201)
        if j <= 78:
            return '3'
        elif j <= 127 and j > 78:
            return '2-1'
        elif j <= 134 and j > 127:
            return '2-2'
        elif j <= 151 and j > 134:
            return '2-3'
        elif j > 151:
            return '1'

def getPlatinumSymbol(probs, r_full=0):
    if r_full:
        i = np.random.randint(1, sum(probs[:10])+1)
    else:
        i = np.random.randint(1, sum(probs)+1)
    if i <= sum(probs[:1]):
        return 'Q'
    elif i <= sum(probs[:2]) and i > sum(probs[:1]):
        return '10'
    elif i <= sum(probs[:3]) and i > sum(probs[:2]):
        return 'K'
    elif i <= sum(probs[:4]) and i > sum(probs[:3]):
        return 'A'
    elif i <= sum(probs[:5]) and i > sum(probs[:4]):
        return 'J'
    elif i <= sum(probs[:6]) and i > sum(probs[:5]):
        return 'Ca'
    elif i <= sum(probs[:7]) and i > sum(probs[:6]):
        return 'Cr'
    elif i <= sum(probs[:8]) and i > sum(probs[:7]):
        return 'D'
    elif i <= sum(probs[:9]) and i > sum(probs[:8]):
        return 'Co'
    elif i <= sum(probs[:10]) and i > sum(probs[:9]):
        return 'W'
    elif i > sum(probs[:10]):
        return 'R'

def getWeightedProbability(game):
    weight = [27, 25, 24, 23, 19, 19, 18, 16, 15, 8, 6]
    switch = [0] * 11
    unique_list = list(set(game))
    for n, s in enumerate(labels):
        if s in unique_list:
            switch[n] = 2
        if s != 'R' and game.count(s) >= 6:
            switch[n] = 5
    probs = [w*(switch[n]+1) for n, w in enumerate(weight)]
    return probs

def spin_platinum():
    game = []
    r_full = 0
    for i in range(5):
        probs = getWeightedProbability(game)
        tmp = []
        if game.count('R') >= 9:
            r_full = 1
        col_type = getPlatinumColType(i)
        if col_type == '3':
            for i in range(3):
                tmp.append(getPlatinumSymbol(probs, r_full))
        elif col_type == '2-1':
            tmp.extend([getPlatinumSymbol(probs, r_full)]*2)
            tmp.append(getPlatinumSymbol(probs, r_full))
        elif col_type == '2-2':
            tmp.extend([getPlatinumSymbol(probs, r_full)]*2)
            tmp.append(getPlatinumSymbol(probs, r_full))
            tmp[2], tmp[1] = tmp[1], tmp[2]
        elif col_type == '2-3':
            tmp.append(getPlatinumSymbol(probs, r_full))
            tmp.extend([getPlatinumSymbol(probs, r_full)]*2)
        elif col_type == '1':
            tmp.extend([getPlatinumSymbol(probs, r_full)]*3)
        game.extend(tmp)
    return game

def getSym(lst):
    if len(set(lst)) < 2:
        return lst[0]
    else:
        for x in list(set(lst)):
            if x != 'W':
                return x
            else:
                continue

def richCheck(game, bpl):
    rnum = game.count('R')
    if rnum <= 2:
        return 0
    elif rnum == 3:
        return bpl * 30
    elif rnum == 4:
        return bpl * 90
    elif rnum == 5:
        return bpl * 240
    elif rnum == 6:
        return bpl * 900
    elif rnum == 7:
        return bpl * 2250
    elif rnum == 8:
        return bpl * 15000
    elif rnum >= 9:
        return bpl * 30000

def calPlatinumPayline(game, bpl):
    pay = 0
    # r_acc += 1
    pay_type_list = []
    
    # RICH 보너스 계산
    pay += richCheck(game, bpl)
    
    '''
    # RICH 누적 보너스 계산
    if r_acc >= 100:
        r_acc = 0
        pay += bpl * np.random.randint(1000, 1201) 
    '''
    btrigger = np.random.randint(1, 101)
    if btrigger == 1:
         pay += bpl * np.random.randint(1100, 1201)
    
    # payline 계산
    for payline in paylines:
        tmp = []
        for i in range(5):
            if i == 4:
                tmp.append(game[payline[i]])
                break
            if i == 0 and game[payline[i]] == 'W':
                tmp.append(game[payline[i]])
            elif game[payline[i]] != game[payline[i+1]] and game[payline[i+1]] != 'W':
                tmp.append(game[payline[i]])
                break
            else:
                tmp.append(game[payline[i]])
        if len(tmp) <= 2:
            tmp = []
        else:
            sym = getSym(tmp)
            pay += payTable.loc[len(tmp)-3, sym] * bpl
        pay_type_list.append(tmp)
    return pay, pay_type_list

def playPlatinum(n, bpl):
    r_acc = 0
    pay_list = []
    pay_type_list = []
    while(n):
        game = spin_platinum()
        pay_list.append(calPlatinumPayline(game, bpl)[0])
        pay_type_list.append(calPlatinumPayline(game, bpl)[1])
        n -= 1
    return pay_list, pay_type_list

### ----------- ###
r_acc = 0
simul_pay_list, simul_pay_type_list = playPlatinum(2000, 2000)

sampling_pay = []
for i in range(20):
    simul_pay_list, simul_pay_type_list = playPlatinum(2000, 2000)
    sampling_pay.append(sum(simul_pay_list) / len(simul_pay_list))
    
sum(sampling_pay) / len(sampling_pay)

print('Simulation Average Reward : ', sum(simul_pay_list) / len(simul_pay_list))

real_pay_list, real_pay_type_list = [], []

for t_game in test_game:
    real_pay_list.append(calPlatinumPayline(t_game, 2000)[0])
    real_pay_type_list.append(calPlatinumPayline(t_game, 2000)[1])

print('Real Average Reward : ', sum(real_pay_list) / len(real_pay_list))


### ----- 쓰레기통 ------ ###

'''
def getPlatinumColType():
    i = np.random.randint(1, 201)
    if i <= 109:
        return 3
    elif i <= 186 and i > 109:
        return 2
    elif i > 186:
        return 1
'''


'''
def getPlatinumSymbol(start, end):
    i = np.random.randint(start, end)
    if i <= 27:
        return 'Q'
    elif i <= 52 and i > 27:
        return '10'
    elif i <= 76 and i > 52:
        return 'K'
    elif i <= 99 and i > 76:
        return 'A'
    elif i <= 118 and i > 99:
        return 'J'
    elif i <= 137 and i > 118:
        return 'Ca'
    elif i <= 155 and i > 137:
        return 'Cr'
    elif i <= 171 and i > 155:
        return 'D'
    elif i <= 186 and i > 171:
        return 'Co'
    elif i <= 192 and i > 186:
        return 'W'
    elif i > 192:
        return 'R'
'''


'''
def calPayline():
    pay = 0
    for payline in paylines:
        count = 0
        for i in range(5):
            if payline[i] != 'W':
                sym = game[payline[i]]
                break
        for n, i in enumerate(payline):
            if game[payline[n]] == 'W':
                count += 1
                if count == 5:
                    pay += payTable.loc[count-3,sym]
                    break
                continue
            if game[payline[n]] != game[payline[n+1]]:
                if n <= 1:
                    break
                else:
                    pay += payTable.loc[count-2,sym]
                    break
            if n == 4:
                pay += payTable.loc[count-2,sym]
            count += 1
'''
