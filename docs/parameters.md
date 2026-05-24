# Parameters

Full reference for the `awc()` function.

---

## Signature

```python
from AnimatedWordCloud import awc

awc(text, time, date_format, max_words, ngram, color,
    freq, stopwords, skip, frames, numbers, punct, fix_encoding, title)
```

---

## Parameter reference

### `text`

| Property | Value |
|----------|-------|
| Type | `pd.Series` |
| Required | Yes |

A pandas Series containing the text column of your dataset.

```python
awc(text=data['review'], ...)
```

---

### `time`

| Property | Value |
|----------|-------|
| Type | `pd.Series` |
| Required | Yes |

A pandas Series containing the corresponding timestamp for each text entry.

```python
awc(time=data['date'], ...)
```

---

### `date_format`

| Property | Value |
|----------|-------|
| Type | `str` |
| Options | `'us'`, `'eur'` |
| Required | Yes |

Date format of the `time` column.

| Value | Interpretation | Examples |
|-------|---------------|---------|
| `'us'` | MM/DD/YYYY | `12/31/2013`, `Feb-09-2009` |
| `'eur'` | DD/MM/YYYY | `31/12/2013`, `09-Feb-2009` |

---

### `max_words`

| Property | Value |
|----------|-------|
| Type | `int` |
| Recommended | `50`–`200` |
| Required | Yes |

Maximum number of words to display simultaneously in the animation.

---

### `ngram`

| Property | Value |
|----------|-------|
| Type | `int` |
| Options | `1`, `2` |
| Required | Yes |

N-gram size:

- `1` — unigrams (individual words)
- `2` — bigrams (two-word phrases)

---

### `color`

| Property | Value |
|----------|-------|
| Type | `str` |
| Options | `'black'`, `'white'` |
| Required | Yes |

Background color of the animation.

---

### `freq`

| Property | Value |
|----------|-------|
| Type | `str` |
| Options | `'Y'`, `'M'` |
| Required | Yes |

Frequency of aggregation:

- `'Y'` — yearly (one frame group per year)
- `'M'` — monthly (one frame group per month)

---

### `stopwords`

| Property | Value |
|----------|-------|
| Type | `list` of `str` |
| Required | Yes |

List of stopword language sets to apply. Uses the `arabica` stopword library.

Common values: `['english']`, `['english', 'german']`, `['english', 'french', 'spanish']`

Pass an empty list to skip stopword removal:

```python
stopwords=[]
```

---

### `skip`

| Property | Value |
|----------|-------|
| Type | `list` of `str` or `None` |
| Default | `None` |
| Required | Yes |

Custom list of additional words to remove (on top of stopwords). Set to `None` to skip.

```python
skip=['said', 'also', 'however']
```

---

### `frames`

| Property | Value |
|----------|-------|
| Type | `int` |
| Recommended | `40`–`100` |
| Required | Yes |

Number of animation frames rendered **per time period**. Higher values produce smoother transitions but take longer to render.

---

### `numbers`

| Property | Value |
|----------|-------|
| Type | `bool` |
| Required | Yes |

- `True` — remove numeric tokens from the text
- `False` — keep numbers as words

---

### `punct`

| Property | Value |
|----------|-------|
| Type | `bool` |
| Required | Yes |

- `True` — strip punctuation
- `False` — keep punctuation

---

### `fix_encoding`

| Property | Value |
|----------|-------|
| Type | `bool` |
| Required | Yes |

- `True` — apply `ftfy` encoding fix (useful for scraped web text or multilingual data)
- `False` — skip encoding correction

---

### `title`

| Property | Value |
|----------|-------|
| Type | `str` |
| Required | Yes |

Base name for output files. Used as the MP4 filename and the prefix for the Excel statistics files.

```python
title='ecb_speeches_2024'
```

Output: `postprocessing/ecb_speeches_2024.mp4`

---

## Complete example

```python
awc(text         = data['text'],
    time         = data['date'],
    date_format  = 'us',
    max_words    = 100,
    ngram        = 1,
    color        = 'black',
    freq         = 'Y',
    stopwords    = ['english'],
    skip         = ['said', 'also'],
    frames       = 80,
    numbers      = True,
    punct        = True,
    fix_encoding = False,
    title        = 'my_animation')
```
