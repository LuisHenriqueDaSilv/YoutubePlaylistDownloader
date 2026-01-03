# 📺 YouTube Playlist Downloader CLI

A high-performance, aesthetically pleasing command-line interface (CLI) designed for seamless YouTube playlist archival. Built with Python, this tool leverages the industry-standard `yt-dlp` engine and the `Rich` library to provide a modern, dashboard-like experience directly in your terminal.

## 🚀 What is it?

The **YouTube Playlist Downloader** is more than just a simple script; it's a robust utility designed for users who value both efficiency and visual feedback. It automates the process of fetching metadata and downloading entire playlists while maintaining a clear, real-time overview of the progress.

### Key Features

- **Smart Metadata Extraction**: Fast, non-blocking playlist parsing.
- **Concurrent-like UI**: Uses `Rich's` `Live` display to show overall progress alongside individual file status.
- **Robustness**: Graceful error handling for missing videos or network interruptions.
- **Customization**: Easily specify output directories and formats.

## 📦 Dependencies

The project relies on a minimal but powerful stack:

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: The engine used for video extraction and downloading.
- **[Rich](https://github.com/Textualize/rich)**: Used for the professional UI, progress bars, tables, and panels.
- **[Typer](https://typer.tiangolo.com/)**: Provides the CLI structure and elegant argument parsing.
- **[FFmpeg](https://ffmpeg.org/)** (Recommended): Required by `yt-dlp` for merging high-quality video and audio streams seamlessly.

To install the Python dependencies:

```bash
pip install -r requirements.txt
```

## 🛠 How to Run

Running the downloader is straightforward thanks to the `Typer` implementation.

### Basic Usage

To download a playlist using default settings:

```bash
python downloader.py download "PLAYLIST_URL"
```

### Custom Output Directory

Specify where you want the videos to be saved:

```bash
python downloader.py download "PLAYLIST_URL" --output ./my_videos
```

### Help System

View all available options:

```bash
python downloader.py --help
```

## 🧠 How it Works

This project follows a professional software engineering pattern, separating UI concerns from the core download logic.

### 1. Metadata Extraction

The process begins with the `get_playlist_info` function.

- **Tool**: `yt_dlp.YoutubeDL` with `extract_flat: True`.
- **Logic**: This fetches the list of video titles and URLs without immediately downloading them, allowing the tool to display a summary table and initialize the progress bars accurately.

### 2. Modern Terminal UI

The interface is built using a combination of `Rich` components:

- **`Panel.fit`**: Displays a professional header.
- **`Table`**: Lists all videos found in the playlist before starting the download.
- **`Progress` Hooks**: Two separate progress bars are managed:
  - **Overall Progress**: Tracks the number of videos completed.
  - **Current Video Progress**: Shows bytes downloaded, speed, and ETA for the active file.
- **`Live` Display**: Wraps both progress objects in a `Group` to update the terminal screen smoothly at 10Hz without flickering.

### 3. Asynchronous Progress Tracking

Instead of using standard `yt-dlp` logging, the project implements a custom `RichProgressHook` class.

- **`__call__` Method**: This hook is triggered by `yt-dlp` during the download. It extracts `downloaded_bytes` and `total_bytes` from the status dictionary and updates the `Rich` progress task in real-time.

### 4. CLI Architecture

By using `Typer`, the application benefits from:

- Type hints for command-line arguments.
- Automatic generation of `--help` menus.
- Clean entry point via `app()` in the `if __name__ == "__main__":` block.

---

_Developed with focus on DX (Developer Experience) and visual excellence._
# YoutubePlaylistDownloader
