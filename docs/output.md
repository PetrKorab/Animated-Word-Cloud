# Output Files

AnimatedWordCloud saves all output to a `postprocessing/` folder inside your working directory.

---

## Directory layout

```
your_project/
├── your_script.py          # or notebook.ipynb
└── postprocessing/
    ├── my_animation.mp4    # ← main output video
    ├── my_animation_before_normalisation.xlsx
    ├── my_animation_after_normalisation.xlsx
    ├── frames/             # PNG frames (kept for inspection)
    │   ├── frame_0001.png
    │   ├── frame_0002.png
    │   └── ...
    ├── ffmpeg/             # ffmpeg binary (auto-downloaded)
    │   └── bin/
    │       └── ffmpeg.exe
    └── frames2video.bat    # batch script (auto-downloaded)
```

---

## Output files

### `<title>.mp4`

The main animation video. Frames are stitched into an MP4 using the bundled `ffmpeg` binary.

- Format: H.264 MP4
- Resolution: 1280 × 720 px
- Frame rate: derived from the `frames` parameter

---

### `<title>_before_normalisation.xlsx`

Excel workbook with word frequencies **before** the normalisation step, one sheet per time period.

Columns:

| Column | Description |
|--------|-------------|
| `word` | Token or bigram |
| `count` | Raw occurrence count |

---

### `<title>_after_normalisation.xlsx`

Excel workbook with word frequencies **after** normalisation and clipping to `max_words`, one sheet per time period.

Columns:

| Column | Description |
|--------|-------------|
| `word` | Token or bigram |
| `count` | Normalised frequency score |

---

### `frames/`

Individual PNG frames captured during the physics simulation. They are retained after video creation, useful for:

- Extracting a single still from the animation
- Debugging rendering issues
- Creating GIFs with external tools

---

## Notes

!!! tip "Re-running the animation"
    Delete the `frames/` folder and the `.mp4` file before re-running with the same `title` to avoid mixing frames from previous runs.

!!! info "Auto-downloaded resources"
    `ffmpeg/` and `frames2video.bat` are downloaded once on the first import and reused on subsequent runs. Do not delete them unless you want to trigger a fresh download.
