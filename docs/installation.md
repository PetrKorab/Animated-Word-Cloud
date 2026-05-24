# Installation

## Requirements

- Python **3.8** (3.8.x only)
- Windows (the bundled `ffmpeg.exe` and `frames2video.bat` are Windows binaries)

---

## Install from PyPI

```bash
pip install AnimatedWordCloud
```

---

## Auto-download of ffmpeg

AnimatedWordCloud does **not** bundle `ffmpeg` in the wheel (keeping the package lightweight). Instead, on the very first `import` the package automatically downloads:

- `postprocessing/ffmpeg/` — the ffmpeg binary bundle
- `postprocessing/frames2video.bat` — the batch script that calls ffmpeg

into the **current working directory**.

```python
from AnimatedWordCloud import awc   # ffmpeg downloads here if not already present
```

You will see:

```
AnimatedWordCloud: ffmpeg not found — downloading resources automatically ...
============================================================
AnimatedWordCloud - Downloading post-install resources
============================================================
...
✓ Extracted 90 ffmpeg files to .../postprocessing/ffmpeg
============================================================
Resource download complete.
============================================================
```

If the download fails (e.g. no internet access), a warning is printed but the import still succeeds. You can retry manually:

```python
from AnimatedWordCloud.downloader import download_resources
download_resources()          # downloads into ./postprocessing/
download_resources("my_dir")  # downloads into my_dir/postprocessing/
```

Or via the console script installed with the package:

```bash
animated-wordcloud-setup
animated-wordcloud-setup --dir my_project/
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| [pygame](https://pypi.org/project/pygame) | 2.5.0+ | Visualization and animation rendering |
| [Box2D](https://pypi.org/project/Box2D) | 2.3.10+ | Physics-based word movement |
| [arabica](https://pypi.org/project/Arabica/) | 1.7.7 | Text preprocessing and n-gram extraction |
| [ftfy](https://pypi.org/project/ftfy) | 6.1.1+ | Text encoding correction |
| [openpyxl](https://pypi.org/project/openpyxl) | 3.1.5+ | Excel statistics export |
| [requests](https://pypi.org/project/requests) | any | Post-install resource download |

All dependencies are installed automatically by pip.

---

## Development install

Clone the repository and install in editable mode:

```bash
git clone https://github.com/PetrKorab/Animated-Word-Cloud.git
cd Animated-Word-Cloud
pip install -e .
```
