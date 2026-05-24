# AnimatedWordCloud

[![pypi](https://img.shields.io/pypi/v/AnimatedWordCloud.svg)](https://pypi.org/project/AnimatedWordCloud/)
[![License: Apache 2.0](https://badgen.net/badge/license/apache-2-0/blue)](https://opensource.org/license/apache-2-0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Animated version of classic word cloud for time-series text data**

---

Classic word cloud graphs show which words appear most frequently in a corpus — but they cannot show how language changes over time. **AnimatedWordCloud** solves this by producing a single MP4 video that animates word frequency evolution across multiple time periods.

The physics-based animation engine (words float and collide realistically) was pioneered by Michael Kane in the [WordSwarm](https://github.com/thisIsMikeKane/WordSwarm) project. AnimatedWordCloud wraps it into a clean, pip-installable Python package with full support for unigrams, bigrams, custom stopwords, and both yearly and monthly aggregations.

---

## Key features

| Feature | Details |
|---------|---------|
| **Time-aware** | Yearly (`Y`) or monthly (`M`) frequency aggregation |
| **N-gram support** | Unigrams and bigrams |
| **Color themes** | Black or white background |
| **Auto-scaling** | Intelligent frequency normalization and clipping |
| **Jupyter ready** | Works in `.ipynb` notebooks and `.py` scripts |
| **Auto-download** | `ffmpeg` and `frames2video.bat` downloaded on first import |
| **Statistics export** | Before/after Excel files with normalization stats |

---

## Quick install

```bash
pip install AnimatedWordCloud
```

On first `import`, the package automatically downloads `ffmpeg` and `frames2video.bat` into a `postprocessing/` folder in your working directory — no manual setup required.

---

## Quick start

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

The output MP4 is saved to `postprocessing/my_word_cloud.mp4`.

---

## Links

- [GitHub repository](https://github.com/PetrKorab/Animated-Word-Cloud)
- [PyPI package](https://pypi.org/project/AnimatedWordCloud/)
- [Issues & feedback](https://github.com/PetrKorab/Animated-Word-Cloud/issues)
