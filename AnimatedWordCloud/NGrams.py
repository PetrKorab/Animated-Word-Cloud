import pandas as pd
import sys
from datetime import datetime
from ftfy import fix_encoding

class wsNGrams:
    words = []
    counts_df = pd.read_csv('matrix.csv')
    counts_df.iloc[1:, 0] = counts_df.iloc[1:, 0].apply(fix_encoding)
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
        counts_df.iloc[1:, 0] = counts_df.iloc[1:, 0].apply(fix_encoding)
        test = counts_df.reset_index(drop=True)
        test = test.iloc[0:, 0]
        test = test.dropna()
        words_list = list(test)
        for item in words_list:
            self.words.append(item)

        dates_list = list(counts_df.columns.values)[1:]
        for item in dates_list:
            # Try multiple date formats
            item = item.strip()
            date_parsed = False
            
            # Try year-only format first (e.g., '2000')
            try:
                item = datetime.strptime(item, '%Y')
                item = item.date()
                self.dates.append(item)
                date_parsed = True
            except ValueError:
                pass
            
            # If that failed, try year-month format (e.g., '2000-01')
            if not date_parsed:
                for fmt in ['%Y-%m', '%Y-%m-%d']:
                    try:
                        item = datetime.strptime(item, fmt)
                        item = item.date()
                        self.dates.append(item)
                        date_parsed = True
                        break
                    except ValueError:
                        continue
            
            # If still not parsed, raise an error with helpful message
            if not date_parsed:
                raise ValueError(f"Cannot parse date '{item}'. Expected formats: YYYY, YYYY-MM, or YYYY-MM-DD")