import os
import sys
import yt_dlp
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    TaskID,
)
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
import typer
from typing import Optional
from pathlib import Path

app = typer.Typer(help="YouTube Playlist Downloader CLI")
console = Console()

def get_playlist_info(url: str):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            if 'entries' not in info:
                return None
            return info
        except Exception as e:
            console.print(f"[bold red]Error fetching playlist info:[/bold red] {e}")
            return None

class RichProgressHook:
    def __init__(self, progress: Progress, task_id: TaskID):
        self.progress = progress
        self.task_id = task_id

    def __call__(self, d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            if total > 0:
                self.progress.update(self.task_id, completed=downloaded, total=total)
            
            speed = d.get('speed')
            eta = d.get('eta')
        
        elif d['status'] == 'finished':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            self.progress.update(self.task_id, completed=total, total=total)

@app.command()
def download(
    url: str = typer.Argument(..., help="The URL of the YouTube playlist"),
    output: Optional[Path] = typer.Option(
        Path("./output"), 
        "--output", "-o", 
        help="Destination folder for downloads"
    )
):
    """
    Download all videos from a YouTube playlist with detailed progress.
    """
    console.print(Panel.fit("[bold blue]YouTube Playlist Downloader[/bold blue]", border_style="blue"))
    
    output.mkdir(parents=True, exist_ok=True)
    
    with console.status("[bold green]Fetching playlist information..."):
        playlist_info = get_playlist_info(url)
    
    if not playlist_info:
        console.print("[bold red]Failed to retrieve playlist information. Please check the URL.[/bold red]")
        raise typer.Exit(code=1)

    title = playlist_info.get('title', 'Unknown Playlist')
    entries = list(playlist_info.get('entries', []))
    num_videos = len(entries)

    console.print(f"\n[bold]Playlist:[/bold] {title}")
    console.print(f"[bold]Total Videos:[/bold] {num_videos}")
    console.print(f"[bold]Output Directory:[/bold] {output.absolute()}\n")

    table = Table(title="Videos in Playlist", show_header=True, header_style="bold magenta")
    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    
    for i, entry in enumerate(entries, 1):
        table.add_row(str(i), entry.get('title', 'N/A'))
    
    console.print(table)
    console.print("")

    overall_progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed}/{task.total} videos)"),
    )
    
    video_progress = Progress(
        TextColumn("  [progress.description]{task.description}"),
        BarColumn(bar_width=40),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    )

    overall_task = overall_progress.add_task("Total Progress", total=num_videos)
    
    from rich.console import Group
    from rich.live import Live

    with Live(Group(overall_progress, video_progress), refresh_per_second=10):
        for i, entry in enumerate(entries, 1):
            video_url = entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
            video_title = entry.get('title', f"Video {i}")
            
            display_title = (video_title[:47] + '...') if len(video_title) > 50 else video_title
            
            video_task = video_progress.add_task(f"Downloading: {display_title}", total=None)
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': str(output / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [RichProgressHook(video_progress, video_task)],
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                
                overall_progress.update(overall_task, advance=1)
                video_progress.remove_task(video_task)
            except Exception as e:
                overall_progress.update(overall_task, advance=1)
                video_progress.update(video_task, description=f"[red]Error: {display_title}")

    console.print("\n[bold green]✔ All downloads completed![/bold green]")

if __name__ == "__main__":
    app()
