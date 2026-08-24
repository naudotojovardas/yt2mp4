#!/usr/bin/env python3
"""
YouTube Video Downloader (MP4)
--------------------------------
Downloads YouTube videos as MP4 files using yt-dlp.

Setup (run once in a VS Code terminal):
    pip install yt-dlp

    You also need ffmpeg installed and on your PATH (yt-dlp uses it to
    merge separate video/audio streams into a single MP4 file):
      - Windows:  choco install ffmpeg   (or download from ffmpeg.org)
      - macOS:    brew install ffmpeg
      - Linux:    sudo apt install ffmpeg

Usage:
    python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
    python youtube_downloader.py "URL1" "URL2" "URL3"
    python youtube_downloader.py "URL" -o "C:/Videos" -q 720

Notes:
    - Only download videos you have the right to download (your own
      content, content that's public domain/Creative Commons, or where
      the platform/creator explicitly permits it). Respect YouTube's
      Terms of Service and copyright law.
"""

import argparse
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    sys.exit(
        "yt-dlp is not installed.\n"
        "Run this in your terminal first:\n"
        "    pip install yt-dlp"
    )


def build_format_string(quality: str) -> str:
    """
    Build a yt-dlp format selector that grabs the best available VIDEO
    stream plus the best available AUDIO stream (regardless of source
    container) and merges them. The final file is converted to MP4
    by the postprocessor below, so this deliberately does NOT filter
    on ext=mp4 here -- that filter can silently exclude YouTube's
    highest-resolution streams, which are often VP9/AV1 in WebM.

    "bestvideo+bestaudio" explicitly requires a real video-only stream
    plus a real audio-only stream, so you never end up with an
    audio-only file even if some format is missing on YouTube's end.
    """
    if quality == "best":
        return "bestvideo+bestaudio/best"
    # e.g. quality="720" -> cap height at 720p
    return f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"


def download_videos(urls, output_dir: str, quality: str) -> None:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "format": build_format_string(quality),
        "merge_output_format": "mp4",
        "outtmpl": str(Path(output_dir) / "%(title)s.%(ext)s"),
        "noplaylist": True,       # set to False if you want playlist support
        "quiet": False,
        "no_warnings": False,
        "postprocessors": [
            {
                # Ensures the final file is a proper .mp4 even if
                # source streams came in a different container.
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            print(f"\n--- Downloading: {url} ---")
            try:
                ydl.download([url])
            except yt_dlp.utils.DownloadError as e:
                print(f"Failed to download {url}: {e}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos as MP4 using yt-dlp."
    )
    parser.add_argument("urls", nargs="+", help="One or more YouTube video URLs")
    parser.add_argument(
        "-o", "--output", default="D:\\Vids",
        help="Output directory (default: ./D:\\Vids)"
    )
    parser.add_argument(
        "-q", "--quality", default="best",
        help="Max resolution, e.g. 1080, 720, 480, or 'best' (default: best)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    download_videos(args.urls, args.output, args.quality)
    print("\nDone.")


if __name__ == "__main__":
    main()