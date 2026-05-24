from .preprocessing import prep
from .wsWordObj_monthly import *
from .wsWordObj import *
from .framework.framework import main


class awc():
    def __init__(self, text, time, date_format, max_words, freq, ngram, color, stopwords, skip, frames, numbers, punct, fix_encoding, title):
        print("=" * 60)
        print("ANIMATED WORD CLOUD - Starting")
        print("=" * 60)
        
        self.text = text
        self.time = time
        self.date_format = date_format
        self.max_words = max_words
        self.freq = freq
        self.ngram = ngram
        self.color = color
        self.stopwords = stopwords
        self.skip = skip
        self.frames = frames
        self.numbers = numbers
        self.punct = punct
        self.fix_encoding = fix_encoding
        self.title = title
        # Automatically hide title in all frames
        self.show_title = False

        print(f"Configuration:")
        print(f"  - Max words: {max_words}")
        print(f"  - N-gram: {ngram}")
        print(f"  - Frequency: {freq}")
        print(f"  - Color scheme: {color}")
        print(f"  - Frames per period: {frames}")
        print(f"  - Title: {title}")
        print()

        text = text.dropna()
        print(f"Text data loaded: {len(text)} entries")

        # Convert skip to empty list if None
        skip_list = skip if skip is not None else []
        
        print("Starting text preprocessing...")
        output = prep(text_prep=text, time=time, date_format=date_format, max_words = max_words, ngram=ngram, freq=freq, stopwords=stopwords, skip=skip_list, numbers=numbers, punct=punct, fix_encoding=self.fix_encoding)
        output = output.replace('_', ' ', regex=True)

        output.to_csv("matrix.csv", index=False, encoding="utf8")
        print("✓ Preprocessing complete - matrix.csv created")
        print(f"  Matrix shape: {output.shape[0]} words × {output.shape[1]-1} time periods")
        print()
        print(f"Configuration: freq='{freq}', color='{self.color}'")
        print()

        # Prepare frames argument
        frames_arg = ['-f', str(self.frames)]
        title_arg = ['-t', self.title]
        show_title_arg = [] if self.show_title else ['-x']
        
        if freq == "Y":
            if self.color =='black':
                print("Loading WordSwarm_black (Yearly frequency)...")
                from .WordSwarm_black import WordSwarm
                print("Starting animation generation...")
                main(WordSwarm, frames_arg + title_arg + show_title_arg)

            elif self.color == 'white':
                print("Loading WordSwarm_white (Yearly frequency)...")
                from .WordSwarm_white import WordSwarm
                print("Starting animation generation...")
                main(WordSwarm, frames_arg + title_arg + show_title_arg)
            else:
                print(f"ERROR: Unknown color '{self.color}' for freq='Y'")
                
        elif freq == "M":
            if self.color =='black':
                print("Loading WordSwarm_monthly_black (Monthly frequency)...")
                from .WordSwarm_monthly_black import WordSwarm
                print("Starting animation generation...")
                main(WordSwarm, frames_arg + title_arg + show_title_arg)

            elif self.color == 'white':
                print("Loading WordSwarm_monthly_white (Monthly frequency)...")
                from .WordSwarm_monthly_white import WordSwarm
                print("Starting animation generation...")
                main(WordSwarm, frames_arg + title_arg + show_title_arg)

        else:
            print(""""Incorrect frequency specification Use "Y" or "M" """)
