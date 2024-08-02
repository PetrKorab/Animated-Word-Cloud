[![pypi](https://img.shields.io/pypi/v/AnimatedWordCloud.svg)](https://pypi.python.org/pypi/AnimatedWordCloud)
[![License: MIT](https://badgen.net/badge/license/apache-2-0/blue)]([https://opensource.org/licenses/MIT](https://opensource.org/license/apache-2-0/))


# AnimatedWordCloud
**Animated version of classic word cloud for time-series text data**

Classic word cloud graph does not consider the time variation in text data. Animated word cloud improves on this and displays text datasets collected over multiple periods in a single MP4 file.
The core framework for the animation of word frequencies was developed by Michael Kane in the [WordsSwarm](https://github.com/thisIsMikeKane/WordSwarm) project. **AnimatedWordCloud** makes 
the codes efficiently work on various text datasets of the Latin alphabet languages.

## Installation

It requires **Python 3.8**, [Box2D](https://pypi.org/project/Box2D), [beautifulsoup4](https://pypi.org/project/beautifulsoup4),
[pygame](https://pypi.org/project/pygame), [PyQt6](https://pypi.org/project/PyQt6) - visualization,
[Arabica](https://pypi.org/project/Arabica/) and [ftfy ](https://pypi.org/project/ftfy) for text preprocessing. 

To install using pip, use:

`pip install AnimatedWordCloud`


AnimatedWordCloud has been tested with **PyCharm** community ed. It's recommended to use this IDE and run .py files instead .ipynb.

## Usage

* **Import the library**:

``` python
from AnimatedWordCloud import animated_word_cloud
```

* **Generate frames:**

**animated_word_cloud** generates 200 png word cloud images per period. It scales word frequencies to display word clouds on text datasets of different sizes. Frames are stored in the working directory in the newly created *.post_processing/frames*  folder. It currently provides unigram frequencies (bigram frequencies will be added later). It reads dates in:

* **US-style**: *MM/DD/YYYY* (2013-12-31, Feb-09-2009, 2013-12-31 11:46:17, etc.)
* **European-style**: *DD/MM/YYYY* (2013-31-12, 09-Feb-2009, 2013-31-12 11:46:17, etc.) date and datetime formats.


It automatically cleans data from punctuation and numbers on input. It can also remove the standard list(s) of stopwods for languages in the [NLTK](https://www.nltk.org) corpus of stopwords.


``` python
def animated_word_cloud(text: str,         # Text
                        time: str,         # Time
                        date_format: str,  # Date format: 'eur' - European, 'us' - American
                        ngram: int,        # N-gram order, 1 = unigram, 2 = bigram     
                        freq: str ,        # Aggregation period: 'Y'/'M'
                        stopwords: [],     # Languages for stop words
                        skip: []           # Remove additional stop words 
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
                    ngram = 1,                                   # Show individual word frequencies
                    freq ='Y',                                   # Yearly frequency
                    stopwords = ['english', 'german','french'],  # Clean from English, German and French stop words
                    skip = ['good', 'bad','yellow'])             # Remove 'good', 'bad', and 'yellow' as additional stop words                                                               

```


* **Create video from frames:**

Download the *ffmpeg* folder and the *frames2video.bat* file from [here](https://github.com/PetrKorab/Animated-Word-Cloud/blob/main/frames2video.bat) and place them into the *postprocessing* folder.  Next, run *frames2video.bat*, which will generate a *wordSwarmOut.mp4* file, which is the desired output.

[![AnimatedWordCloud](https://github.com/PetrKorab/AnimatedWordCloud/raw/main/screenshot.png)](https://github.com/PetrKorab/AnimatedWordCloud)


## Documentation, examples and tutorials

* For more examples of coding, read these  tutorials:

> [Data Storytelling with Animated Word Clouds](https://medium.com/towards-data-science/data-storytelling-with-animated-word-clouds-1889fdeb97b8?sk=fc0435e61392f6aad2ec32133600ecf1) 

* Here are examples of animated word clouds:

> [Research Trends in Economics](https://www.youtube.com/watch?v=-2gH7Xfn0AI&t=51s)

> [Amazon Dog Food Reviews](https://www.youtube.com/watch?v=gaqLaRwEAR8)

> [European Central Bankers' speeches](https://www.youtube.com/watch?v=oOgEpGtsJaI) 

---

Please visit [here](https://github.com/PetrKorab/AnimatedWordCloud/issues) for any questions, issues, bugs, and suggestions.
