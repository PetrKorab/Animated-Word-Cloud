[![pypi](https://img.shields.io/pypi/v/AnimatedWordCloud.svg)](https://pypi.python.org/pypi/AnimatedWordCloud)
[![License: MIT](https://badgen.net/badge/license/apache-2-0/blue)]([https://opensource.org/licenses/MIT](https://opensource.org/license/apache-2-0/))


# AnimatedWordCloud
**Animated version of classic word cloud for time-series text data**

Classic word cloud graph does not consider the time variation in text data. Animated word cloud improves on this and displays text datasets collected over multiple periods in a single MP4 file.
The core framework for the animation of word frequencies was developed by Michael Kane in the [WordsSwarm](https://github.com/thisIsMikeKane/WordSwarm) project. **AnimatedWordCloud** makes 
the codes efficiently work on various text datasets of the Latin alphabet languages.

## Installation

It requires **Python 3.8+**, with the following dependencies:
- [pygame](https://pypi.org/project/pygame) 2.5.0+ - for visualization and animation
- [Box2D](https://pypi.org/project/Box2D) 2.3.10+ - for physics-based word movement
- [Arabica](https://pypi.org/project/Arabica/) 1.7.7+ - for text preprocessing and n-gram extraction
- [ftfy](https://pypi.org/project/ftfy) 6.1.1+ - for fixing text encoding issues
- [streamlit](https://pypi.org/project/streamlit) 1.37.0+ - for optional web interface
- [openpyxl](https://pypi.org/project/openpyxl) 3.1.5+ - for Excel file export 

To install the package using pip, use:

`pip install AnimatedWordCloud`

For development version (this repository), install dependencies:

`pip install -r requirements.txt`

The required dependencies are:
```
streamlit==1.37.0
pygame==2.5.0
ftfy==6.1.1
arabica==1.7.7
Box2D==2.3.10
openpyxl==3.1.5
```

AnimatedWordCloud has been tested with **PyCharm** community ed. and VS Code. It's recommended to use a Python IDE and run .py files instead of .ipynb notebooks for better performance.

## Usage

* **Import the library**:

For the package version:
``` python
from AnimatedWordCloud import animated_word_cloud
```

For development version (this repository):
``` python
from animated_word_cloud import awc
```

* **Generate frames:**

**animated_word_cloud** generates customizable png word cloud images per period (default: 80 frames). It automatically scales word frequencies to display word clouds on text datasets of different sizes. Frames are stored in the working directory in the newly created *postprocessing/frames* folder. It supports both unigram (single words) and bigram (two-word phrases) frequencies. It reads dates in:

* **US-style**: *MM/DD/YYYY* (2013-12-31, Feb-09-2009, 2013-12-31 11:46:17, etc.)
* **European-style**: *DD/MM/YYYY* (2013-31-12, 09-Feb-2009, 2013-31-12 11:46:17, etc.) date and datetime formats.


It can automatically clean data from punctuation and numbers. It can also remove the standard list(s) of stopwords for languages in the [NLTK](https://www.nltk.org) corpus of stopwords. The preprocessing pipeline now includes:

* **Automatic frequency normalization**: Scales word frequencies to optimal ranges for visualization
* **Frequency clipping**: Prevents over-representation of extremely common words
* **Statistics export**: Generates Excel files with before/after clipping statistics
* **Enhanced text cleaning**: Improved handling of special characters, dashes, and encoding issues


``` python
def animated_word_cloud(text: str,           # Text column
                        time: str,           # Time/date column
                        date_format: str,    # Date format: 'eur' - European, 'us' - American
                        max_words: int,      # Maximum number of top words/bigrams to display
                        ngram: int,          # N-gram order: 1 = unigram, 2 = bigram     
                        color: str,          # Background color: 'black' or 'white'
                        freq: str,           # Aggregation period: 'Y' (yearly) / 'M' (monthly)
                        stopwords: [],       # Languages for stop words (from NLTK corpus)
                        skip: [],            # Remove additional custom stop words (can be None)
                        frames: int,         # Number of frames per period (default: 80)
                        numbers: bool,       # Remove numbers from text (True/False)
                        punct: bool,         # Remove punctuation from text (True/False)
                        fix_encoding: bool,  # Fix encoding issues (True/False)
                        title: str           # Video filename (without .mp4 extension)
) 
```

To apply the method, use:

``` python
import pandas as pd
data = pd.read_csv("data.csv")
```


``` python
animated_word_cloud(text = data['text'],                         # Read text column
                    time = data['date'],                         # Read date column
                    date_format = 'us',                          # Specify date format
                    max_words = 100,                             # Show top 100 words/bigrams
                    ngram = 1,                                   # Show individual word frequencies (1=words, 2=bigrams)
                    color = 'black',                             # Black background (alternative: 'white')
                    freq = 'Y',                                  # Yearly frequency (alternative: 'M' for monthly)
                    stopwords = ['english', 'german','french'],  # Clean from English, German and French stop words
                    skip = ['good', 'bad','yellow'],             # Remove 'good', 'bad', and 'yellow' as additional stop words
                    frames = 80,                                 # Generate 80 frames per period
                    numbers = True,                              # Remove numbers from text
                    punct = True,                                # Remove punctuation from text
                    fix_encoding = False,                        # Do not fix encoding (set to True if needed)
                    title = 'my_word_cloud')                     # Output filename (without .mp4 extension)

```

### Using Bigrams (Two-Word Phrases):

To analyze two-word phrases instead of individual words, set `ngram = 2`:

``` python
animated_word_cloud(text = data['text'],
                    time = data['date'],
                    date_format = 'eur',
                    max_words = 100,
                    ngram = 2,                               # Use bigrams
                    color = 'black',
                    freq = 'M',                              # Monthly frequency
                    stopwords = ['english'],
                    skip = None,
                    frames = 80,
                    numbers = True,
                    punct = True,
                    fix_encoding = False,
                    title = 'bigram_analysis')
```

Bigrams are particularly useful for:
- Identifying common phrases and collocations
- Understanding multi-word expressions
- Capturing domain-specific terminology
- Analyzing sentiment through phrase patterns

### Key Parameters Explained:

* **max_words**: Controls the number of top words/bigrams to display. Higher values show more words but may affect visualization clarity.
* **ngram**: Set to `1` for single words or `2` for two-word phrases (bigrams). Bigrams are useful for capturing multi-word expressions and phrases.
* **color**: Choose between `'black'` or `'white'` background. Dark backgrounds work better for light-colored text, while white backgrounds are ideal for presentations.
* **frames**: Number of animation frames per time period. Default is 80. Higher values create smoother animations but increase processing time.
* **numbers**: When `True`, removes all numeric values from the text. Set to `False` to keep numbers if they're meaningful in your analysis.
* **punct**: When `True`, removes punctuation marks. Enhanced to handle special characters like em-dashes (—), en-dashes (–), and other non-standard punctuation.
* **fix_encoding**: Set to `True` if your text contains encoding issues (e.g., garbled characters, incorrect Unicode). Uses ftfy library for automatic correction.
* **title**: Specifies the output video filename (without extension). Also used for labeling the animation.

### Output Files:

The function automatically generates several output files:

* **postprocessing/frames/**: Directory containing all generated PNG frames
* **matrix.csv**: Processed frequency matrix used for visualization
* **words_[freq]_before_clipping.xlsx**: Original word frequencies
* **words_[freq]_after_clipping.xlsx**: Normalized frequencies with statistics sheet
* **bigram_[freq]_before_clipping.xlsx**: Original bigram frequencies (when ngram=2)
* **bigram_[freq]_after_clipping.xlsx**: Normalized bigram frequencies with statistics (when ngram=2)

The statistics sheet includes:
- Maximum frequency before/after normalization
- Sum of all frequencies
- Words allowed threshold
- Actual word count
- Normalization coefficient





## Documentation, examples and tutorials

* For more examples of coding, read the Docs

---

Please visit [here](https://github.com/PetrKorab/AnimatedWordCloud/issues) for any questions, issues, bugs, and suggestions.
