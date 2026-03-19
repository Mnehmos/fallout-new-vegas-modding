"""
OpenAI TTS Generator for FNV Dialogue
Reads from audio/tts/scripts/*.json, outputs .wav files
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
import typer
from rich.console import Console
from rich.progress import track

load_dotenv()

app = typer.Typer()
console = Console()

REPO_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = REPO_ROOT / "audio" / "tts" / "scripts"
OUTPUT_DIR = REPO_ROOT / "audio" / "tts" / "output"

# FNV-appropriate voice mapping
# OpenAI voices: alloy, echo, fable, onyx, nova, shimmer
VOICE_MAP = {
    "male_gruff": "onyx",
    "male_neutral": "echo",
    "female_neutral": "nova",
    "announcer": "fable",
    "default": "alloy",
}


def get_client():
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[red]Error: OPENAI_API_KEY not set in .env[/red]")
        raise typer.Exit(1)
    return OpenAI(api_key=api_key)


@app.command()
def generate(
    script_file: str = typer.Argument(None, help="Specific script file to process (or all if omitted)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print lines without generating audio"),
):
    """Generate TTS audio from dialogue script files."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if script_file:
        script_files = [SCRIPTS_DIR / script_file]
    else:
        script_files = list(SCRIPTS_DIR.glob("*.json"))

    if not script_files:
        console.print(f"[yellow]No script files found in {SCRIPTS_DIR}[/yellow]")
        console.print("Create a JSON file there using the format in audio/tts/scripts/example.json")
        raise typer.Exit(0)

    client = None if dry_run else get_client()

    for script_path in script_files:
        console.print(f"\n[bold cyan]Processing:[/bold cyan] {script_path.name}")
        with open(script_path) as f:
            script = json.load(f)

        lines = script.get("lines", [])
        mod_name = script.get("mod", "PerkOverhaul")
        npc_id = script.get("npc_id", "unknown")

        out_subdir = OUTPUT_DIR / mod_name / npc_id
        out_subdir.mkdir(parents=True, exist_ok=True)

        for line in track(lines, description=f"  {npc_id}"):
            line_id = line["id"]
            text = line["text"]
            voice_key = line.get("voice", "default")
            voice = VOICE_MAP.get(voice_key, VOICE_MAP["default"])

            out_file = out_subdir / f"{line_id}.wav"

            if dry_run:
                console.print(f"  [{voice}] {line_id}: {text[:60]}...")
                continue

            if out_file.exists():
                console.print(f"  [dim]Skipping {line_id} (exists)[/dim]")
                continue

            response = client.audio.speech.create(
                model="tts-1-hd",
                voice=voice,
                input=text,
            )
            response.stream_to_file(str(out_file))
            console.print(f"  [green]✓[/green] {line_id}.wav")

    console.print("\n[bold green]Done![/bold green]")


@app.command()
def list_voices():
    """Show available voice options and what they sound like."""
    console.print("\n[bold]Available voices:[/bold]")
    for key, voice in VOICE_MAP.items():
        console.print(f"  {key:20} → OpenAI '{voice}'")


if __name__ == "__main__":
    app()
