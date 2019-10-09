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

def getPlatinumColType(i):
    if i==0:
        np.random.randint(1, 201)
        if i <= 109:
            return '3'
        elif i <= 151 and i > 109:
            return '2-1'
        elif i <= 169 and i > 151:
            return '2-2'
        elif i <= 186 and i > 169:
            return '2-3'
        elif i > 186:
            return '1'
    if i==1:
        np.random.randint(1, 201)
        if i <= 88:
            return '3'
        elif i <= 127 and i > 109:
            return '2-1'
        elif i <= 138 and i > 127:
            return '2-2'
        elif i <= 183 and i > 138:
            return '2-3'
        elif i > 183:
            return '1'
    if i==2:
        np.random.randint(1, 201)
        if i <= 93:
            return '3'
        elif i <= 125 and i > 93:
            return '2-1'
        elif i <= 137 and i > 125:
            return '2-2'
        elif i <= 176 and i > 137:
            return '2-3'
        elif i > 176:
            return '1'
    if i==3:
        np.random.randint(1, 201)
        if i <= 110:
            return '3'
        elif i <= 130 and i > 110:
            return '2-1'
        elif i <= 149 and i > 130:
            return '2-2'
        elif i <= 192 and i > 149:
            return '2-3'
        elif i > 192:
            return '1'
    if i==4:
        np.random.randint(1, 201)
        if i <= 78:
            return '3'
        elif i <= 147 and i > 78:
            return '2-1'
        elif i <= 134 and i > 147:
            return '2-2'
        elif i <= 151 and i > 134:
            return '2-3'
        elif i > 151:
            return '1'

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

def spin_platinum():
    game = []
    start = 1
    end = 201
    for i in range(5):
        tmp = []
        if game.count('R') >= 9:
            end = 193
        col_type = getPlatinumColType(i)
        if col_type == '3':
            for i in range(3):
                tmp.append(getPlatinumSymbol(start, end))
        elif col_type == '2-1':
            tmp.extend([getPlatinumSymbol(start, end)]*2)
            tmp.append(getPlatinumSymbol(start, end))
        elif col_type == '2-2':
            tmp.extend([getPlatinumSymbol(start, end)]*2)
            tmp.append(getPlatinumSymbol(start, end))
            tmp[2], tmp[1] = tmp[1], tmp[2]
        elif col_type == '2-3':
            tmp.append(getPlatinumSymbol(start, end))
            tmp.extend([getPlatinumSymbol(start, end)]*2)
        elif col_type == '1':
            tmp.append(getPlatinumSymbol(start, end))
            tmp.extend([getPlatinumSymbol(start, end)]*3)
        game.extend(tmp)
    return game

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
    elif rnum == 9:
        return bpl * 30000

def calPlatinumPayline(game, bpl):
    pay = 0
    r_acc = 0
    pay_type_list = []
    
    # RICH 보너스 계산
    pay += richCheck(game, bpl)
    r_acc += game.count('R')
    
    '''
    # RICH 누적 보너스 계산
    if r_acc >= 100:
        r_acc = 0
        # pay += bpl *  
    '''
    
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
    return pay

def playPlatinum(n, bpl):
    pay_list = []
    while(n):
        game = spin_platinum()
        pay_list.append(calPlatinumPayline(game, bpl))
        n -= 1
    return pay_list
pay_list = playPlatinum(2000, 2000)
sum(pay_list) / len(pay_list)
p_test = []
for t_game in test_game:
    p_test.append(calPlatinumPayline(t_game, 2000))
sum(p_test) / len(p_test)