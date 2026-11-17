"""Bedrock Archive (.brarchive) CLI command interface.

Provides CLI commands to pack folders into .brarchive files, unpack archives,
list archive entries with deduplication statistics, and selectively extract individual files.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import click
from anvil.lib.brarchive import (
    DESCRIPTOR_SIZE,
    HEADER_SIZE,
    BrArchive,
    BrArchiveError,
)


def _format_size(size_bytes: int) -> str:
    """Formats raw byte counts into human-readable strings (B, KB, MB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


@click.command(
    "brarchive",
    help="Pack a folder into a .brarchive, unpack an archive, list contents, or extract files.",
)
@click.argument(
    "action",
    type=click.Choice(
        [
            "pack",
            "p",
            "unpack",
            "u",
            "list",
            "ls",
            "extract",
            "e",
        ],
        case_sensitive=False,
    ),
)
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-o",
    "--out",
    type=click.Path(),
    default=None,
    help="Output file or directory path.",
)
@click.option(
    "--dedup/--no-dedup",
    default=True,
    help="Enable or disable content deduplication when packing.",
)
@click.option(
    "-e",
    "--entry",
    type=str,
    default=None,
    help="Specific entry name to extract (required for 'extract' action).",
)
def brarchive_cmd(
    action: str,
    path: str,
    out: Optional[str],
    dedup: bool,
    entry: Optional[str],
) -> None:
    """Bedrock Archive (.brarchive) CLI management command.

    Actions:
        pack / p:      Packs a directory or file into a .brarchive container.
        unpack / u:    Unpacks a .brarchive file (or folder of archives) to disk.
        list / ls:     Inspects and displays descriptors and deduplication stats.
        extract / e:   Selectively extracts a single entry without unpacking all.
    """
    action = action.lower()
    target_path = Path(path)
    out_path = Path(out) if out else None

    try:
        # Action: Pack folder or file into .brarchive
        if action in ("pack", "p"):
            compiled = BrArchive.pack(target_path, out_path, deduplicate=dedup)
            file_size = compiled.stat().st_size
            click.echo(
                click.style(
                    f"\r[INFO]: Successfully packed to '{compiled}' ({_format_size(file_size)}).",
                    fg="green",
                )
            )

        # Action: Unpack .brarchive into directory
        elif action in ("unpack", "u"):
            extracted = BrArchive.unpack(target_path, out_path)
            click.echo(
                click.style(
                    f"\r[INFO]: Successfully unpacked to '{extracted}'.",
                    fg="green",
                )
            )

        # Action: List archive contents and compute deduplication statistics
        elif action in ("list", "ls"):
            with BrArchive(target_path, mode="r") as arc:
                entries = arc.infolist()
                click.echo(
                    click.style(
                        f"\nArchive: {target_path.name} ({len(entries)} entries)\n",
                        bold=True,
                    )
                )
                click.echo(f"{'Length':>10}  {'Offset':>10}  {'Name'}")
                click.echo("-" * 60)

                total_uncompressed = 0
                for e in entries:
                    total_uncompressed += e.size
                    click.echo(f"{_format_size(e.size):>10}  {e.offset:>10}  {e.name}")

                # Calculate storage savings from deduplication
                archive_size = target_path.stat().st_size
                content_base = HEADER_SIZE + len(entries) * DESCRIPTOR_SIZE
                actual_content_size = max(0, archive_size - content_base)
                savings = max(0, total_uncompressed - actual_content_size)

                click.echo("-" * 60)
                click.echo(f"Total entries:      {len(entries)}")
                click.echo(f"Uncompressed size:  {_format_size(total_uncompressed)}")
                click.echo(f"Archive file size:  {_format_size(archive_size)}")
                if savings > 0 and total_uncompressed > 0:
                    pct = (savings / total_uncompressed) * 100
                    click.echo(
                        f"Deduplication save: {_format_size(savings)} ({pct:.1f}%)"
                    )

        # Action: Selectively extract a single file from the archive
        elif action in ("extract", "e"):
            if not entry:
                click.echo(
                    click.style(
                        "\r[ERROR]: Option '--entry' / '-e' is required for the 'extract' action.",
                        fg="red",
                    ),
                    err=True,
                )
                sys.exit(1)

            dest_dir = out_path if out_path else Path.cwd()
            with BrArchive(target_path, mode="r") as arc:
                extracted_file = arc.extract(entry, dest_dir)
                click.echo(
                    click.style(
                        f"\r[INFO]: Successfully extracted '{entry}' to '{extracted_file}'.",
                        fg="green",
                    )
                )

    except BrArchiveError as e:
        click.echo(
            click.style(
                f"\r[ERROR]: {e}",
                fg="red",
            ),
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        click.echo(
            click.style(
                f"\r[ERROR]: {e}",
                fg="red",
            ),
            err=True,
        )
        sys.exit(1)
