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
def spin():
    for i in range(5):
        reel_type = np.random.randint(200)
        symbol = np.random.randint(100)
def calPayline():
    pay = 0
    for payline in paylines:
        lst = []
        for i in range(5):
            if payline[i] != 'W':
                sym = game[payline[i]]
                break
        for n, i in enumerate(payline):
            lst.append(game[i])
            if len(set(lst)) > 1:
                if n <= 2:
                    break
                else:
                    pay += paytable.loc[sym][n+1]