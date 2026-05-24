from AnimatedWordCloud import awc
import pandas as pd

data = pd.read_excel('MeetupStatsForWordCloud.xlsx') # Read data
   

awc(text = data['text'],                            # Read text column
           time = data['date'],                     # Read date column
           date_format = 'eur',                     # Specify date format
           max_words=100,                           # Show top ngrams
           ngram = 2,                               # N-gram type (1 = words, 2 = bigrams)
           color = 'black',                         # Color background (black/white)
           freq ='Y',                               # Period aggregation (Y=yearly, M=monthly)
           stopwords = ["english"],                 # Clean from NLTK stopwords list
           skip = None,                             # Skip specific words
           frames = 40,                             # Number of frames per period for video
           numbers = True,                          # Remove numbers from text
           punct = True,                            # Remove punctuation from text
           fix_encoding = False,                    # Fix encoding issues
           title = 'Test python')    