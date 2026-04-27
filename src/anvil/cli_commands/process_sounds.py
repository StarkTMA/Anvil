import os
import subprocess
from pathlib import Path

import click

DEFAULT_TARGET_LUFS = -18
DEFAULT_SAMPLE_RATE = "32000"
DEFAULT_QUALITY = "0"


def process_file(
    input_file: Path,
    output_file: Path,
    relative_path: Path,
    target_lufs: float,
    sample_rate: str,
    quality: str,
) -> str:

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write to a temporary file first
    temp_output: Path = output_file.with_suffix(".tmp.ogg")

    ffmpeg_cmd: list[str] = [
        "ffmpeg",
        "-threads",
        "1",
        "-i",
        str(input_file),
        "-af",
        f"loudnorm=I={target_lufs}:LRA=11:TP=-1.5,pan=mono|c0=c0",
        "-c:a",
        "libvorbis",
        "-q:a",
        quality,
        "-ar",
        sample_rate,
        "-map_metadata",
        "-1",
        "-fflags",
        "+bitexact",
        "-flags:v",
        "+bitexact",
        "-flags:a",
        "+bitexact",
        str(temp_output),
        "-y",
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
        # Replace the original file with the processed temp file
        temp_output.replace(output_file)
        return f"Processed: {relative_path}"
    except subprocess.CalledProcessError as e:
        if temp_output.exists():
            temp_output.unlink()
        return f"Error {relative_path}: {e.stderr.decode()}"


@click.command(
    "process-sounds",
    help="Batch process and normalize audio files in assets/sounds (DESTRUCTIVE: overwrites originals).",
)
# Removed threads option
@click.option(
    "--target-lufs",
    default=DEFAULT_TARGET_LUFS,
    show_default=True,
    type=float,
    help="Target LUFS for loudness normalization.",
)
@click.option(
    "--sample-rate",
    default=DEFAULT_SAMPLE_RATE,
    show_default=True,
    help="Sample rate for output audio.",
)
@click.option(
    "--quality",
    default=DEFAULT_QUALITY,
    show_default=True,
    help="Vorbis quality (0-10, higher is better).",
)
def sound(target_lufs, sample_rate, quality) -> None:
    input_root = Path("assets/sounds")
    output_root = Path("assets/sounds")

    click.secho(
        "WARNING: This operation is DESTRUCTIVE and will overwrite all audio files in assets/sounds!",
        fg="red",
        bold=True,
    )
    if not click.confirm("Do you want to continue?", default=False):
        click.echo("Aborted by user.")
        return

    for root, _, files in os.walk(input_root):
        for filename in files:
            if filename.lower().endswith((".wav", ".mp3", ".ogg")):
                input_file: Path = Path(root) / filename
                relative_path: Path = input_file.relative_to(input_root)
                output_file: Path = output_root / relative_path.with_suffix(".ogg")
                result: str = process_file(
                    input_file,
                    output_file,
                    relative_path,
                    target_lufs,
                    sample_rate,
                    quality,
                )
                print(result)
