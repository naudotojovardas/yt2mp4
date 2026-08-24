# YouTube Video Downloader (MP4)

A simple Python tool that downloads YouTube videos as MP4 files, using
[`yt-dlp`](https://github.com/yt-dlp/yt-dlp) under the hood. Comes with
both a command-line script and a double-click Windows launcher.

---

## Table of Contents

1. [Features](#features)
2. [Files in This Project](#files-in-this-project)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
   - [Option A: Command Line](#option-a-command-line)
   - [Option B: Double-Click Launcher (Windows)](#option-b-double-click-launcher-windows)
6. [Command-Line Arguments](#command-line-arguments)
7. [How Quality Selection Works](#how-quality-selection-works)
8. [Where Files Are Saved](#where-files-are-saved)
9. [Customizing Defaults](#customizing-defaults)
10. [Troubleshooting](#troubleshooting)
11. [Legal & Ethical Notice](#legal--ethical-notice)

---

## Features

- Downloads YouTube videos in true MP4 format (video + audio merged, not
  just an audio track).
- Automatically grabs the **best available quality** by default, or lets
  you cap it (e.g. 1080p, 720p).
- Supports downloading multiple URLs in a single run.
- Creates the output folder automatically if it doesn't exist.
- Includes a Windows `.bat` launcher so you don't need to type commands.

---

## Files in This Project

| File                    | Purpose                                                             |
|--------------------------|----------------------------------------------------------------------|
| `youtube_downloader.py`  | The main Python script that does the downloading.                   |
| `download_video.bat`     | Windows double-click launcher — prompts for a URL and runs the script. |
| `README.md`              | This file.                                                           |

Both `yt2mp4.py` and `fast_download.bat` must be kept in the
**same folder** — the launcher depends on the script being right next to it.

---

## Prerequisites

You need three things installed before this will work:

1. **Python 3.8+**
   Check with:
   ```
   python --version
   ```
   If that fails, install Python from [python.org](https://www.python.org/downloads/)
   and make sure to check **"Add Python to PATH"** during setup.

2. **yt-dlp** (Python package that does the actual downloading)
   Installed via pip — see [Installation](#installation) below.

3. **ffmpeg** (merges separate video/audio streams into one MP4 file)
   This is a separate program, not a Python package. See below for
   install instructions per OS.

---

## Installation

### 1. Install yt-dlp

Open a terminal (in VS Code: `` Ctrl+` ``) and run:
```
pip install yt-dlp
```

### 2. Install ffmpeg

**Windows** (via [Chocolatey](https://chocolatey.org/)):
```powershell
# First, install Chocolatey if you don't have it (run in an Administrator PowerShell):
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install ffmpeg:
choco install ffmpeg
```
Alternative: download a build directly from [ffmpeg.org](https://ffmpeg.org/download.html)
and manually add the `bin` folder to your PATH.

**macOS** (via [Homebrew](https://brew.sh/)):
```
brew install ffmpeg
```

**Linux (Debian/Ubuntu):**
```
sudo apt install ffmpeg
```

### 3. Verify everything is installed

```
python --version
yt-dlp --version
ffmpeg -version
```
All three should print version info with no errors. If any command says
"not recognized" or "command not found," see [Troubleshooting](#troubleshooting).

### 4. Get the project files

Place `youtube_downloader.py` and `download_video.bat` in a folder of your
choice, e.g. `D:\py_files\`.

---

## Usage

### Option A: Command Line

Open a terminal, navigate to the folder containing the script, and run:

```
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Replace `VIDEO_ID` with a **real** YouTube video ID — copy the full URL
directly from your browser's address bar while watching the video.

**Download multiple videos at once:**
```
python youtube_downloader.py "URL1" "URL2" "URL3"
```

**Choose a custom output folder:**
```
python youtube_downloader.py "URL" -o "D:/Videos"
```

**Cap the resolution (e.g. to save space):**
```
python youtube_downloader.py "URL" -q 720
```

**Combine options:**
```
python youtube_downloader.py "URL" -o "D:/Videos" -q 1080
```

### Option B: Double-Click Launcher (Windows)

1. Double-click `fast_download.bat`.
2. A console window opens and asks you to paste a YouTube URL.
3. It then asks for a max quality — press **Enter** to just get the best
   available.
4. The video downloads into a `downloads` folder next to the script.
5. Press any key to close the window when it's done.

**Tip:** Right-click `download_video.bat` → **Send to → Desktop (create
shortcut)** to get a desktop icon for one-click access, no terminal needed.

---

## Command-Line Arguments

| Argument            | Required | Default      | Description                                              |
|----------------------|----------|--------------|------------------------------------------------------------|
| `urls`               | Yes      | —            | One or more YouTube video URLs (space-separated).           |
| `-o`, `--output`     | No       | `downloads`  | Folder to save videos into. Created automatically if missing. |
| `-q`, `--quality`    | No       | `best`       | Max resolution (e.g. `1080`, `720`, `480`) or `best`.        |

---

## How Quality Selection Works

The script asks yt-dlp for the best available **video-only** stream and
the best available **audio-only** stream, then merges them into a single
MP4 with ffmpeg:

```python
"bestvideo+bestaudio/best"
```

This is deliberate — YouTube frequently stores its highest resolutions
(1440p, 4K) as VP9/AV1 video in a WebM container, not as native MP4.
By not filtering on `ext=mp4` upfront, the script grabs the actual best
quality YouTube offers, and ffmpeg handles converting/merging it into a
proper `.mp4` file afterward (`merge_output_format: "mp4"` in the code).

The `+` between `bestvideo` and `bestaudio` requires **both** a real
video stream and a real audio stream to be selected — so you'll never
end up with an audio-only file by accident.

When you cap quality with `-q 720`, it becomes:
```
bestvideo[height<=720]+bestaudio/best[height<=720]
```
— best video no taller than 720p, plus best audio.

---

## Where Files Are Saved

By default, videos go into a folder named `downloads`, created **inside
whichever directory you run the script from** (or next to the `.bat`
file, if using the launcher).

Each file is named after the video's title:
```
downloads/
├── Some Video Title.mp4
├── Another Video.mp4
```

To save elsewhere, use `-o "path/to/folder"` on the command line, or see
[Customizing Defaults](#customizing-defaults) to change it permanently.

---

## Customizing Defaults

Open `youtube_downloader.py` in VS Code and find this block near the
bottom of the file:

```python
parser.add_argument(
    "-o", "--output", default="downloads",
    help="Output directory (default: ./downloads)"
)
```

Change `"downloads"` to any path you like, for example:
```python
default="D:/Videos",
```

**Windows path tip:** use forward slashes (`D:/Videos`) or doubled
backslashes (`D:\\Videos`) — a single backslash in a Python string can
be misinterpreted.

You can similarly change the default quality by editing:
```python
parser.add_argument(
    "-q", "--quality", default="best",
    ...
)
```

---

## Troubleshooting

**`yt-dlp is not installed` / `ModuleNotFoundError: No module named 'yt_dlp'`**
Run `pip install yt-dlp` in the same terminal/Python environment you're
using to run the script.

**`can't open file '...youtube_downloader.py': [Errno 2] No such file or directory`**
Python can't find the script at that path. Either:
- `cd` into the folder that actually contains the file, then run it, or
- Double-check the exact path and filename (use `dir /s /b youtube_downloader.py`
  on Windows to search your drives for it).

**`Incomplete YouTube ID VIDEO_ID` / `URL looks truncated`**
You ran the command with the literal placeholder text `VIDEO_ID` still
in it. Replace it with a real video URL copied from your browser, e.g.
`https://www.youtube.com/watch?v=dQw4w9WgXcQ`.

**`ffmpeg is not recognized` / merging fails**
ffmpeg isn't installed or isn't on your PATH. Revisit the
[Installation](#installation) section, and after installing, **close and
reopen your terminal** (and VS Code, if applicable) so it picks up the
updated PATH.

**`python is not recognized as an internal or external command`**
Python isn't on your PATH. Reinstall Python from python.org and check
"Add Python to PATH" during setup, or use the full path to your
`python.exe` (e.g. `C:\Users\user\AppData\Local\Programs\Python\Python314\python.exe`)
in place of `python` in commands.

**Download works but the video is very low resolution**
Some videos genuinely don't have higher-resolution streams available.
Try without `-q` (or with a higher cap) to confirm you're getting the
best available, not an artificially limited one.

**Video downloads but has no sound, or vice versa**
This shouldn't happen with the current format string
(`bestvideo+bestaudio`), since it requires both streams. If it does
happen, check the console output for ffmpeg errors during the merge step
— it likely means ffmpeg isn't installed correctly.

**Playlist URL only downloads one video**
This is intentional — the script sets `noplaylist: True` so a video
inside a playlist link downloads just that one video. To download whole
playlists, this would need a small code change (ask if you'd like it).

---

## Legal & Ethical Notice

Only download videos you actually have the right to download — for
example, your own uploads, content explicitly marked as public domain
or Creative Commons, or videos where the creator/platform has given
permission. Downloading copyrighted content without permission may
violate YouTube's Terms of Service and copyright law in your
jurisdiction. This tool is provided for legitimate personal use cases
(e.g. archiving your own content, offline viewing of permitted material)
— you're responsible for how you use it. 
