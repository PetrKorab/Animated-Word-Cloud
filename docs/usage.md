# Usage

## Import

```python
from AnimatedWordCloud import awc
```

On first import, `ffmpeg` and `frames2video.bat` are downloaded automatically into `postprocessing/` in the current working directory.

---

## Minimal example

```python
import pandas as pd
from AnimatedWordCloud import awc

data = pd.read_csv("data.csv")

awc(text        = data['text'],
    time        = data['date'],
    date_format = 'us',
    max_words   = 100,
    ngram       = 1,
    color       = 'black',
    freq        = 'Y',
    stopwords   = ['english'],
    skip        = None,
    frames      = 80,
    numbers     = True,
    punct       = True,
    fix_encoding= False,
    title       = 'my_word_cloud')
```

The MP4 is saved to `postprocessing/my_word_cloud.mp4`.

---

## Unigram example (yearly)

Analyse individual word frequencies, aggregated by year:

```python
import pandas as pd
from AnimatedWordCloud import awc

data = pd.read_csv("speeches.csv")

awc(text        = data['text'],
    time        = data['date'],
    date_format = 'us',
    max_words   = 100,
    ngram       = 1,             # individual words
    color       = 'black',
    freq        = 'Y',           # yearly aggregation
    stopwords   = ['english', 'german', 'french'],
    skip        = ['said', 'also'],
    frames      = 80,
    numbers     = True,
    punct       = True,
    fix_encoding= False,
    title       = 'speech_trends')
```

---

## Bigram example (monthly)

Analyse two-word phrase frequencies, aggregated by month:

```python
import pandas as pd
from AnimatedWordCloud import awc

data = pd.read_excel("reviews.xlsx")

awc(text        = data['review'],
    time        = data['date'],
    date_format = 'eur',         # DD/MM/YYYY
    max_words   = 100,
    ngram       = 2,             # two-word phrases
    color       = 'white',
    freq        = 'M',           # monthly aggregation
    stopwords   = ['english'],
    skip        = None,
    frames      = 60,
    numbers     = True,
    punct       = True,
    fix_encoding= False,
    title       = 'review_bigrams')
```

---

## Jupyter notebook

AnimatedWordCloud works in Jupyter notebooks:

```python
import pandas as pd
from AnimatedWordCloud import awc   # ffmpeg auto-downloaded on first cell run

data = pd.read_excel('MeetupStatsForWordCloud.xlsx')

awc(text        = data['text'],
    time        = data['date'],
    date_format = 'eur',
    max_words   = 100,
    ngram       = 2,
    color       = 'black',
    freq        = 'Y',
    stopwords   = ['english'],
    skip        = None,
    frames      = 40,
    numbers     = True,
    punct       = True,
    fix_encoding= False,
    title       = 'Ethereum_Y_words')
```

!!! tip
    Run the notebook from a directory that does **not** already contain a `postprocessing/` folder to trigger the auto-download and verify everything is working end-to-end.

---

## Supported date formats

| Style | Format | Examples |
|-------|--------|---------|
| US (`'us'`) | MM/DD/YYYY | `2013-12-31`, `Feb-09-2009`, `2013-12-31 11:46:17` |
| European (`'eur'`) | DD/MM/YYYY | `2013-31-12`, `09-Feb-2009`, `2013-31-12 11:46:17` |

---

## Tips

- **Large datasets (>10 000 rows):** use `max_words=50` and `freq='Y'` to keep processing fast.
- **Monthly vs yearly:** `freq='M'` works best for datasets spanning 1–3 years; use `freq='Y'` for longer periods.
- **Smoothness vs speed:** `frames=40` is fast; `frames=80–100` produces smoother animations.
- **Encoding issues:** set `fix_encoding=True` if you see garbled characters (uses the `ftfy` library).
- **Stopwords:** always remove common words for the language(s) in your dataset to reveal meaningful terms.
