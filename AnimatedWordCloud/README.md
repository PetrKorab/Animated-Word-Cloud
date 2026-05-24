[![pypi](https://img.shields.io/pypi/v/AnimatedWordCloud.svg)](https://test.pypi.org/project/AnimatedWordCloud/)
[![License: Apache 2.0](https://badgen.net/badge/license/apache-2-0/blue)](https://opensource.org/license/apache-2-0/)

# AnimatedWordCloud

**Animated version of classic word cloud for time-series text data**

Classic word cloud graphs do not capture how language changes over time. AnimatedWordCloud improves on this by displaying text datasets collected over multiple periods in a single MP4 file. The core physics-based animation framework was developed by Michael Kane in the [WordSwarm](https://github.com/thisIsMikeKane/WordSwarm) project.

---

## Installation

Requires **Python 3.8+**.

```bash
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            AnimatedWordCloud
```

After installation, download the required `ffmpeg` binary and `frames2video.bat` into your working directory:

```python
from AnimatedWordCloud.downloader import download_resources
download_resources()
```

Or via the console script:

```bash
animated-wordcloud-setup
```

This creates a `postprocessing/` folder containing `ffmpeg/bin/ffmpeg.exe` and `frames2video.bat`.

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| [pygame](https://pypi.org/project/pygame) | 2.5.0+ | Visualization and animation rendering |
| [Box2D](https://pypi.org/project/Box2D) | 2.3.10+ | Physics-based word movement |
| [arabica](https://pypi.org/project/Arabica/) | 1.7.7 | Text preprocessing and n-gram extraction |
| [ftfy](https://pypi.org/project/ftfy) | 6.1.1+ | Text encoding correction |
| [openpyxl](https://pypi.org/project/openpyxl) | 3.1.5+ | Excel statistics export |
| [requests](https://pypi.org/project/requests) | any | Post-install resource download |

---

## Quick Start

```python
import pandas as pd
from AnimatedWordCloud import awc

data = pd.read_csv("data.csv")

awc(text        = data['text'],
    time        = data['date'],
    date_format = 'us',          # 'us' or 'eur'
    max_words   = 100,
    ngram       = 1,             # 1 = words, 2 = bigrams
    color       = 'black',       # 'black' or 'white'
    freq        = 'Y',           # 'Y' = yearly, 'M' = monthly
    stopwords   = ['english'],
    skip        = None,
    frames      = 80,
    numbers     = True,
    punct       = True,
    fix_encoding= False,
    title       = 'my_word_cloud')
```

The MP4 is written to `postprocessing/<title>.mp4` in the current working directory.

---

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | Series | Text column from your DataFrame |
| `time` | Series | Date/time column |
| `date_format` | str | `'us'` (MM/DD/YYYY) or `'eur'` (DD/MM/YYYY) |
| `max_words` | int | Number of top words/bigrams to display |
| `ngram` | int | `1` for unigrams, `2` for bigrams |
| `color` | str | `'black'` or `'white'` background |
| `freq` | str | `'Y'` (yearly) or `'M'` (monthly) aggregation |
| `stopwords` | list | NLTK stopword language(s), e.g. `['english', 'french']` |
| `skip` | list / None | Additional words to remove |
| `frames` | int | Animation frames per time period (default: 80) |
| `numbers` | bool | Remove numbers from text |
| `punct` | bool | Remove punctuation from text |
| `fix_encoding` | bool | Auto-fix encoding issues via ftfy |
| `title` | str | Output video filename (without `.mp4`) |

### Date formats supported

- **US**: `MM/DD/YYYY` — `2013-12-31`, `Feb-09-2009`, `2013-12-31 11:46:17`
- **European**: `DD/MM/YYYY` — `2013-31-12`, `09-Feb-2009`, `2013-31-12 11:46:17`

---

## Bigram example

```python
awc(text        = data['text'],
    time        = data['date'],
    date_format = 'eur',
    max_words   = 100,
    ngram       = 2,             # two-word phrases
    color       = 'black',
    freq        = 'M',
    stopwords   = ['english'],
    skip        = None,
    frames      = 80,
    numbers     = True,
    punct       = True,
    fix_encoding= False,
    title       = 'bigram_analysis')
```

---

## Output files

| File / Folder | Description |
|---------------|-------------|
| `postprocessing/<title>.mp4` | Final animation video |
| `postprocessing/frames/` | Individual PNG frames |
| `matrix.csv` | Processed word-frequency matrix |
| `words_[Y/M]_before_clipping.xlsx` | Raw frequencies |
| `words_[Y/M]_after_clipping.xlsx` | Normalized frequencies + statistics |
| `bigram_[Y/M]_before_clipping.xlsx` | Raw bigram frequencies (ngram=2) |
| `bigram_[Y/M]_after_clipping.xlsx` | Normalized bigram frequencies + statistics |

---

## Package structure

```
AnimatedWordCloud/
├── __init__.py                  # Exports awc
├── animated_word_cloud.py       # Main awc class
├── preprocessing.py             # Text cleaning and n-gram pipeline
├── NGrams.py                    # Yearly frequency matrix
├── NGrams_monthly.py            # Monthly frequency matrix
├── WordSwarm_black.py           # Yearly black-background animation
├── WordSwarm_white.py           # Yearly white-background animation
├── WordSwarm_monthly_black.py   # Monthly black-background animation
├── WordSwarm_monthly_white.py   # Monthly white-background animation
├── wsWordObj.py                 # FreeType word rendering (yearly)
├── wsWordObj_monthly.py         # FreeType word rendering (monthly)
├── colorer.py                   # HSV word colouring
├── settings.py                  # Framework settings
├── downloader.py                # Post-install ffmpeg/bat downloader
└── framework/
    ├── framework.py             # Box2D simulation base + main()
    ├── pygame_framework.py      # Pygame renderer
    ├── pygame_gui.py            # Pygame GUI widgets
    └── settings.py              # Physics and display settings
```

---

## Links

- [GitHub repository](https://github.com/PetrKorab/Animated-Word-Cloud)
- [Tutorial: Data Storytelling with Animated Word Clouds](https://medium.com/towards-data-science/data-storytelling-with-animated-word-clouds-1889fdeb97b8)
- [Example: ECB Speeches](https://www.youtube.com/watch?v=oOgEpGtsJaI)
- [Example: Amazon Reviews](https://www.youtube.com/watch?v=gaqLaRwEAR8)
- [Issues & feedback](https://github.com/PetrKorab/AnimatedWordCloud/issues)
