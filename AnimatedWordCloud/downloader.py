"""
Post-install resource downloader for AnimatedWordCloud.

Downloads the ffmpeg binary bundle and frames2video.bat from the
AnimatedWordCloud GitHub repository into a target directory (defaults
to the current working directory).  These files are NOT bundled in the
PyPI wheel to keep the package lightweight.

Usage (Python):
    from AnimatedWordCloud.downloader import download_resources
    download_resources()          # downloads into the current directory
    download_resources("my_dir")  # downloads into my_dir/

Usage (console script after pip install):
    animated-wordcloud-setup
"""

import os
import io
import zipfile
import sys

REPO_ZIP_URL = "https://github.com/PetrKorab/Animated-Word-Cloud/archive/refs/heads/main.zip"
FRAMES2VIDEO_URL = "https://raw.githubusercontent.com/PetrKorab/Animated-Word-Cloud/main/frames2video.bat"

FFMPEG_PREFIX = "Animated-Word-Cloud-main/ffmpeg/"
FRAMES2VIDEO_FILENAME = "frames2video.bat"


def download_resources(target_dir="."):
    """
    Download ffmpeg/ directory and frames2video.bat from the
    AnimatedWordCloud GitHub repository.

    Parameters
    ----------
    target_dir : str
        Directory into which postprocessing/ffmpeg/ and frames2video.bat
        will be written.  Created if it does not exist.
    """
    try:
        import requests
    except ImportError:
        print("ERROR: 'requests' package is required. Install it with: pip install requests")
        sys.exit(1)

    target_dir = os.path.abspath(target_dir)
    postprocessing_dir = os.path.join(target_dir, "postprocessing")
    ffmpeg_dir = os.path.join(postprocessing_dir, "ffmpeg")
    frames_dir = os.path.join(postprocessing_dir, "frames")

    os.makedirs(ffmpeg_dir, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)

    print("=" * 60)
    print("AnimatedWordCloud - Downloading post-install resources")
    print("=" * 60)
    print(f"Target directory: {target_dir}")
    print()

    # ------------------------------------------------------------------
    # 1. Download frames2video.bat
    # ------------------------------------------------------------------
    bat_dest = os.path.join(postprocessing_dir, FRAMES2VIDEO_FILENAME)
    print(f"Downloading {FRAMES2VIDEO_FILENAME} ...")
    try:
        resp = requests.get(FRAMES2VIDEO_URL, timeout=30)
        resp.raise_for_status()
        with open(bat_dest, "wb") as f:
            f.write(resp.content)
        print(f"  ✓ Saved to {bat_dest}")
    except Exception as e:
        print(f"  WARNING: Could not download frames2video.bat: {e}")

    # ------------------------------------------------------------------
    # 2. Download the full repo zip and extract ffmpeg/ subtree
    # ------------------------------------------------------------------
    print(f"\nDownloading ffmpeg bundle from GitHub (this may take a moment)...")
    try:
        resp = requests.get(REPO_ZIP_URL, timeout=120, stream=True)
        resp.raise_for_status()

        raw = b""
        for chunk in resp.iter_content(chunk_size=65536):
            raw += chunk

        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            ffmpeg_entries = [
                name for name in zf.namelist()
                if name.startswith(FFMPEG_PREFIX) and not name.endswith("/")
            ]

            if not ffmpeg_entries:
                print("  WARNING: No ffmpeg files found in the GitHub archive.")
                print(f"  Expected files under '{FFMPEG_PREFIX}' inside the zip.")
            else:
                extracted = 0
                for entry in ffmpeg_entries:
                    relative = entry[len(FFMPEG_PREFIX):]
                    dest_path = os.path.join(ffmpeg_dir, relative.replace("/", os.sep))
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    with zf.open(entry) as src, open(dest_path, "wb") as dst:
                        dst.write(src.read())
                    extracted += 1

                print(f"  ✓ Extracted {extracted} ffmpeg files to {ffmpeg_dir}")

    except Exception as e:
        print(f"  WARNING: Could not download or extract ffmpeg bundle: {e}")
        print("  Please manually download ffmpeg from:")
        print("  https://github.com/PetrKorab/Animated-Word-Cloud/tree/main/ffmpeg")
        print(f"  and place it at: {ffmpeg_dir}")

    print()
    print("=" * 60)
    print("Resource download complete.")
    print(f"  postprocessing/ffmpeg/  → {ffmpeg_dir}")
    print(f"  postprocessing/frames2video.bat → {bat_dest}")
    print("=" * 60)


def _auto_download(target_dir="."):
    """
    Called automatically on package import.

    Checks whether ffmpeg and frames2video.bat are already present in
    target_dir/postprocessing/.  If either is missing the full
    download_resources() routine is invoked so the user never needs to
    run a separate setup step.  Network failures produce a warning but
    never raise an exception so the import always succeeds.
    """
    ffmpeg_exe = os.path.join(
        target_dir, "postprocessing", "ffmpeg", "bin", "ffmpeg.exe"
    )
    bat_file = os.path.join(
        target_dir, "postprocessing", FRAMES2VIDEO_FILENAME
    )
    if os.path.exists(ffmpeg_exe) and os.path.exists(bat_file):
        return
    print("AnimatedWordCloud: ffmpeg not found — downloading resources automatically ...")
    try:
        download_resources(target_dir)
    except Exception as e:
        print(f"AnimatedWordCloud: WARNING — could not download resources automatically: {e}")
        print("  To retry manually run:")
        print("    from AnimatedWordCloud.downloader import download_resources")
        print("    download_resources()")


def main():
    """Entry point for the 'animated-wordcloud-setup' console script."""
    import argparse
    parser = argparse.ArgumentParser(
        description="Download AnimatedWordCloud post-install resources (ffmpeg + frames2video.bat)"
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="Target directory (default: current working directory)",
    )
    args = parser.parse_args()
    download_resources(args.dir)


if __name__ == "__main__":
    main()
