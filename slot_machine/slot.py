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

col_type = [[3], [2, 1], [1, 1, 1]]

payTable = pd.read_csv('../data/slot_machine/platinum_csv/payTable.csv')
game = ['Co', 'K', 'D', 'K', 'K', 'K', 'K', 'A', 'Co', 'Q', 'A', 'R', 'Ca', 'Ca', 'Ca']

def get_col_type():
    i = np.random.randint(1, 201)
    if i <= 109:
        return 3
    elif i <= 186 and i > 109:
        return 2
    elif i > 186:
        return 1

def get_symbol():
    i = np.random.randint(1, 201)
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
    elif i <= 194 and i > 186:
        return 'R'
    elif i > 194:
        return 'W'

def spin_platinum():
    game = []
    for i in range(5):
        tmp = []
        col_type = get_col_type()
        if col_type == 3:
            print(col_type)
            for i in range(col_type):
                tmp.append(get_symbol())
        elif col_type == 2:
            print(col_type)
            tmp.extend([get_symbol()]*2)
            tmp.append(get_symbol())
            np.random.shuffle(tmp)
        else:
            print(col_type)
            tmp.extend([get_symbol(np.random.randint(1, 201))]*3)
        game.extend(tmp)
    return game

game = spin_platinum()

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
def calPayline2():
    pay = 0
    for payline in paylines:
        count = 0
        tmp = []
        for i in range(5):
            tmp.append(game[payline[i]])
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