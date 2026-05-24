# Examples

A collection of animations and tutorials created with AnimatedWordCloud.

---

## Video demos

### Research Trends in Economics

Word frequency trends extracted from academic economics papers over several decades.

<iframe width="100%" height="400" src="https://www.youtube.com/embed/-2gH7Xfn0AI?start=51" frameborder="0" allowfullscreen></iframe>

---

### Amazon Dog Food Reviews

Customer review language evolution from Amazon product reviews.

<iframe width="100%" height="400" src="https://www.youtube.com/embed/gaqLaRwEAR8" frameborder="0" allowfullscreen></iframe>

---

### European Central Bankers' Speeches

Monthly animated word cloud of ECB press conference transcripts, tracking shifts in monetary policy language.

<iframe width="100%" height="400" src="https://www.youtube.com/embed/oOgEpGtsJaI" frameborder="0" allowfullscreen></iframe>

---

## Tutorials

### Data Storytelling with Animated Word Clouds

Step-by-step tutorial on Medium (Towards Data Science) covering:

- Loading and preparing time-stamped text data
- Choosing the right aggregation frequency
- Customising stopwords for domain-specific corpora
- Interpreting the output

[Read on Medium](https://medium.com/towards-data-science/data-storytelling-with-animated-word-clouds-1889fdeb97b8){ .md-button }

---

## Code snippets

### ECB Speeches — monthly bigrams

```python
import pandas as pd
from AnimatedWordCloud import awc

data = pd.read_excel('ecb_speeches.xlsx')

awc(text         = data['text'],
    time         = data['date'],
    date_format  = 'eur',
    max_words    = 100,
    ngram        = 2,
    color        = 'black',
    freq         = 'M',
    stopwords    = ['english', 'german', 'french'],
    skip         = None,
    frames       = 80,
    numbers      = True,
    punct        = True,
    fix_encoding = False,
    title        = 'ecb_bigrams')
```

---

### Amazon reviews — yearly unigrams (white background)

```python
import pandas as pd
from AnimatedWordCloud import awc

data = pd.read_csv('amazon_dog_food.csv')

awc(text         = data['review'],
    time         = data['date'],
    date_format  = 'us',
    max_words    = 80,
    ngram        = 1,
    color        = 'white',
    freq         = 'Y',
    stopwords    = ['english'],
    skip         = ['product', 'food', 'dog'],
    frames       = 60,
    numbers      = True,
    punct        = True,
    fix_encoding = False,
    title        = 'amazon_reviews')
```

---

## Share your animation

Created a cool word cloud animation? Open a [GitHub Discussion](https://github.com/PetrKorab/Animated-Word-Cloud/discussions) or mention [@PetrKorab](https://github.com/PetrKorab) — we'd love to feature it here.
