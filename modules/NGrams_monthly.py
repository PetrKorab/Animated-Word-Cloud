import pandas as pd
import sys
from datetime import datetime

class wsNGrams:
    words = []
    counts_df = pd.read_csv('matrix.csv')
    counts=counts_df.to_numpy()
    dates = []
    areColors = False
    colors = None
    nDates = len(counts_df.columns) - 1
    nWords = len(counts_df) - 1
    topN = sys.maxsize
    maxCount = 64

    def __init__(self, fName, startDateStr, endDateStr, topN):
        counts_df = pd.read_csv('matrix.csv')
        test = counts_df.reset_index(drop=True)
        test = test.iloc[0:, 0]
        test = test.dropna()
        words_list = list(test)
        for item in words_list:
            self.words.append(item)

        dates_list = list(counts_df.columns.values)[1:]
        for item in dates_list:
            item = datetime.strptime(item, '%Y-%m')
            item = item.date()
            self.dates.append(item)