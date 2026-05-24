import pandas as pd
import sys
from datetime import datetime
import numpy as np

class wsNGrams:
    words = []
    counts_df = pd.read_csv('matrix.csv', encoding='utf-8')
    counts=counts_df.to_numpy()
    dates = []
    areColors = False
    colors = None
    nDates = len(counts_df.columns) - 1
    nWords = len(counts_df) - 1
    topN = sys.maxsize
    maxCount = 64
    maxFrequencyCap = 100  # Testing variable: cap frequencies at this value

    def __init__(self, fName, startDateStr, endDateStr, topN):
        print("Loading frequency data from matrix.csv...")
        counts_df = pd.read_csv('matrix.csv', encoding='utf-8')
        
        print(f"  Raw data: {len(counts_df)} words × {len(counts_df.columns)-1} time periods")
        
        # Cap all frequency values at maxFrequencyCap
        print(f"  Capping frequencies at {self.maxFrequencyCap}...")
        numeric_cols = counts_df.columns[1:]  # All columns except the first (words column)
        for col in numeric_cols:
            counts_df[col] = counts_df[col].clip(upper=self.maxFrequencyCap)
        
        # Update counts array with capped values
        self.counts = counts_df.to_numpy()
        
        # Recalculate maxCount based on capped values
        numeric_data = counts_df.iloc[:, 1:].values  # All numeric columns
        self.maxCount = np.max(numeric_data)
        print(f"  Maximum frequency after capping: {self.maxCount}")
        
        print("  Extracting words...")
        test = counts_df.reset_index(drop=True)
        test = test.iloc[0:, 0]
        test = test.dropna()
        words_list = list(test)
        for item in words_list:
            self.words.append(item)

        print(f"  Total words loaded: {len(self.words)}")
        print("  Parsing time periods...")
        
        dates_list = list(counts_df.columns.values)[1:]
        for item in dates_list:
            # Try multiple date formats
            item = item.strip()
            date_parsed = False
            
            # Try year-month format first (e.g., '2000-01' or '2000-1')
            for fmt in ['%Y-%m', '%Y-%m-%d']:
                try:
                    item = datetime.strptime(item, fmt)
                    item = item.date()
                    self.dates.append(item)
                    date_parsed = True
                    break
                except ValueError:
                    continue
            
            # If that failed, try year-only format (e.g., '2000')
            if not date_parsed:
                try:
                    item = datetime.strptime(item, '%Y')
                    item = item.date()
                    self.dates.append(item)
                    date_parsed = True
                except ValueError:
                    pass
            
            # If still not parsed, raise an error with helpful message
            if not date_parsed:
                raise ValueError(f"Cannot parse date '{item}'. Expected formats: YYYY-MM, YYYY-MM-DD, or YYYY")
        
        print(f"  Total time periods loaded: {len(self.dates)}")
        print("✓ N-grams data ready for visualization")
        print()