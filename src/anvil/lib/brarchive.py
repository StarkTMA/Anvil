"""Bedrock Archive (.brarchive) library for Minecraft Bedrock Edition.

The .brarchive format is an uncompressed binary container developed by Mojang
for bundling files inside Bedrock resource and behavior packs.

Binary Layout Specification (Version 1, Little-Endian):
======================================================

1. Header (16 bytes total):
   ┌───────────┬────────┬────────────────────────────────────────────────────────┐
   │ Byte Span │ Type   │ Description                                            │
   ├───────────┼────────┼────────────────────────────────────────────────────────┤
   │ 0x00-0x07 │ uint64 │ Magic number: 0x267052A0B125277D                       │
   │ 0x08-0x0B │ uint32 │ Entry count: number of files stored in the archive     │
   │ 0x0C-0x0F │ uint32 │ Format version: 1                                      │
   └───────────┴────────┴────────────────────────────────────────────────────────┘

2. Descriptor Table (256 bytes per entry):
   Located immediately after the header at byte offset 16 (0x10).
   Total table size = Entry Count * 256 bytes.
   ┌───────────┬──────────┬──────────────────────────────────────────────────────┐
   │ Byte Span │ Type     │ Description                                          │
   ├───────────┼──────────┼──────────────────────────────────────────────────────┤
   │ 0x00      │ uint8    │ Name length (L): 0 to 247 bytes                      │
   │ 0x01-0xF7 │ char[247]│ Relative UTF-8 entry name, zero-padded to 247 bytes  │
   │ 0xF8-0xFB │ uint32   │ Content Offset: start byte relative to Content Base  │
   │ 0xFC-0xFF │ uint32   │ Content Length: size of the file payload in bytes    │
   └───────────┴──────────┴──────────────────────────────────────────────────────┘

3. Content Section:
   Located immediately after the descriptor table at:
     Content Base = 16 + (Entry Count * 256)
   Each entry's raw file bytes start at:
     Absolute Offset = Content Base + Content Offset

Content Deduplication:
---------------------
Because each descriptor specifies its own relative Content Offset and Length,
multiple descriptors (e.g. duplicate textures, sounds, or JSON definitions)
can point to the exact same byte slice in the Content Section. This allows
archives to achieve significant space savings without requiring file compression.
"""

from __future__ import annotations

import fnmatch
import hashlib
import io
import struct
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

# ---------------------------------------------------------------------------
# Format Constants
# ---------------------------------------------------------------------------

# 8-byte magic constant identifying a valid .brarchive file
MAGIC: int = 0x267052A0B125277D

# Supported .brarchive format version
VERSION: int = 1

# Fixed size in bytes of the archive header
HEADER_SIZE: int = 16

# Fixed size in bytes of each entry descriptor record
DESCRIPTOR_SIZE: int = 256

# Maximum permitted byte length for UTF-8 encoded entry paths
MAX_NAME_LEN: int = 247

# Default filename patterns to exclude when compiling directories
DEFAULT_EXCLUDES: tuple[str, ...] = (
    ".*",  # Hidden / dotfiles (.git, .DS_Store, etc.)
    "*~",  # Editor backup files
    "*.tmp",  # Temporary files
    "Thumbs.db",  # Windows thumbnail cache
    "desktop.ini",  # Windows folder customization file
)


# ---------------------------------------------------------------------------
# Exception Hierarchy
# ---------------------------------------------------------------------------


class BrArchiveError(Exception):
    """Base exception for all Bedrock Archive operations."""


class BadArchiveError(BrArchiveError):
    """Raised when an archive file is malformed, truncated, or has an invalid header."""


class UnsupportedVersionError(BrArchiveError):
    """Raised when an archive version is unsupported by this library."""


class InvalidEntryError(BrArchiveError):
    """Raised when an entry name or content is invalid (empty, too long, null bytes)."""


class SecurityError(BrArchiveError):
    """Raised when an operation attempts directory traversal or path manipulation."""


# ---------------------------------------------------------------------------
# Metadata Structures
# ---------------------------------------------------------------------------


@dataclass(slots=True, frozen=True)
class ArchiveInfo:
    """Metadata representing a single file entry inside a Bedrock archive.

    Attributes:
        name: Relative POSIX file path inside the archive (e.g. 'textures/dirt.png').
        offset: Byte offset relative to the start of the Content Section.
        size: Length of the file payload in bytes.
    """

    name: str
    offset: int
    size: int

    @property
    def filename(self) -> str:
        """Alias for name, matching standard library ZipInfo conventions."""
        return self.name


# ---------------------------------------------------------------------------
# Path Sanitization & Security Validation
# ---------------------------------------------------------------------------


def sanitize_path(name: str) -> str:
    """Validates and normalizes an entry name into a clean POSIX archive path.

    Performs security and formatting checks:
    - Normalizes Windows backslashes ('\\') to forward slashes ('/').
    - Strips leading and trailing slashes and whitespace.
    - Rejects null bytes ('\\0') which could terminate C strings prematurely.
    - Rejects Windows drive letters (e.g. 'C:') and absolute root paths.
    - Rejects directory traversal segments ('..') to prevent Zip-Slip vulnerabilities.
    - Enforces the 247-byte maximum UTF-8 length constraint.

    Args:
        name: The relative file path to sanitize.

    Returns:
        str: Canonical POSIX archive entry name.

    Raises:
        InvalidEntryError: If the name is empty, too long, or contains null characters.
        SecurityError: If directory traversal or drive letters are detected.
    """
    if not name or not isinstance(name, str):
        raise InvalidEntryError("Archive entry name cannot be empty.")
    if "\0" in name:
        raise InvalidEntryError("Archive entry name cannot contain null characters.")

    # Normalize backslashes and strip outer slashes/whitespace
    clean = name.replace("\\", "/").strip("/ \t\r\n")
    if not clean:
        raise InvalidEntryError("Archive entry name cannot resolve to root.")

    # Block Windows drive letters (e.g. "C:/...", "d:/...")
    if len(clean) >= 2 and clean[1] == ":" and clean[0].isalpha():
        raise SecurityError(f"Entry name cannot contain drive letters: '{name}'")

    # Segment validation: reject ".." traversal and drop redundant "." segments
    parts: list[str] = []
    for part in clean.split("/"):
        p = part.strip()
        if p == "..":
            raise SecurityError(f"Directory traversal detected in entry name: '{name}'")
        if not p or p == ".":
            continue
        parts.append(p)

    if not parts:
        raise InvalidEntryError("Archive entry name resolves to an empty path.")

    canonical = "/".join(parts)
    raw_name = canonical.encode("utf-8")
    if len(raw_name) > MAX_NAME_LEN:
        raise InvalidEntryError(
            f"Entry name exceeds maximum of {MAX_NAME_LEN} bytes: '{canonical}' ({len(raw_name)} bytes)"
        )
    return canonical


def safe_extract_path(dest_root: Path, entry_name: str) -> Path:
    """Resolves and validates that dest_root / entry_name stays within dest_root.

    Protects against Zip-Slip vulnerabilities during extraction by verifying that
    the resolved target path is strictly a descendant of the destination directory.

    Args:
        dest_root: Base destination directory where files will be unpacked.
        entry_name: Relative path of the file entry.

    Returns:
        Path: The validated absolute destination file path.

    Raises:
        SecurityError: If the target path escapes dest_root.
    """
    target = (dest_root / Path(entry_name)).resolve()
    if not target.is_relative_to(dest_root.resolve()):
        raise SecurityError(
            f"Extraction path traversal detected: '{entry_name}' escapes '{dest_root}'"
        )
    return target


# ---------------------------------------------------------------------------
# Bedrock Archive Class
# ---------------------------------------------------------------------------


class BrArchive:
    """Bedrock Archive (.brarchive) container.

    Provides a clean, intuitive interface for reading, creating, modifying,
    and extracting Minecraft Bedrock Edition .brarchive files.

    Basic Usage:
        # 1. Packing a folder:
        BrArchive.pack("path/to/folder", "pack.brarchive")

        # 2. Reading an archive:
        arc = BrArchive("pack.brarchive")
        print(arc.namelist())
        data = arc.read("textures/terrain.png")

        # 3. Unpacking an archive:
        BrArchive.unpack("pack.brarchive", "extracted_folder")

        # 4. In-memory manipulation:
        arc = BrArchive()
        arc.writestr("manifest.json", b'{"format_version": 2}')
        raw_bytes = arc.to_bytes()
    """

    def __init__(
        self,
        source: Path | str | bytes | BinaryIO | None = None,
        *,
        mode: str = "r",
        deduplicate: bool = True,
    ) -> None:
        """Initializes a BrArchive instance.

        Args:
            source: Path to an archive file, raw bytes, file-like stream, or None for a new archive.
            mode: Open mode ('r' for read, 'w' or 'x' for write).
            deduplicate: When True (default), identical file contents share the same byte offset.
        """
        self.deduplicate: bool = deduplicate
        self.entries: dict[str, bytes] = {}
        self._infos: list[ArchiveInfo] = []

        self.mode = mode.rstrip("b")
        self._target: Path | BinaryIO | None = None

        if source is not None:
            if self.mode in ("w", "x"):
                # In write mode, source is treated as the destination target to write to upon close()
                self._target = (
                    Path(source) if isinstance(source, (str, Path)) else source
                )
            else:
                # In read mode, load and parse entries from source
                self.load(source)

    def __enter__(self) -> BrArchive:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()

    def close(self) -> None:
        """Saves changes if an output target was specified in write mode."""
        if self._target is not None:
            if isinstance(self._target, (str, Path)):
                self.save(self._target)
            elif hasattr(self._target, "write"):
                self._target.write(self.to_bytes())

    # --- Container Mapping Protocol ---

    def __len__(self) -> int:
        """Returns the number of file entries in the archive."""
        return len(self.entries)

    def __contains__(self, name: object) -> bool:
        """Checks if a given entry name exists in the archive."""
        if not isinstance(name, str):
            return False
        try:
            return sanitize_path(name) in self.entries
        except (InvalidEntryError, SecurityError):
            return False

    def __iter__(self) -> Iterator[str]:
        """Iterates over all entry names in the archive."""
        return iter(self.entries)

    def __getitem__(self, name: str) -> bytes:
        """Returns the raw byte payload of an entry by name."""
        return self.read(name)

    # --- Reading & Inspection ---

    def namelist(self) -> list[str]:
        """Returns a list of all entry names stored in the archive."""
        return list(self.entries.keys())

    def infolist(self) -> list[ArchiveInfo]:
        """Returns descriptor metadata (name, offset, size) for all archive entries."""
        return list(self._infos)

    def getinfo(self, name: str) -> ArchiveInfo:
        """Retrieves descriptor metadata for a specific entry name.

        Args:
            name: The archive entry name to look up.

        Returns:
            ArchiveInfo: Descriptor containing name, offset, and size.

        Raises:
            KeyError: If the entry is not present in the archive.
        """
        canonical = sanitize_path(name)
        for info in self._infos:
            if info.name == canonical:
                return info
        if canonical in self.entries:
            return ArchiveInfo(
                name=canonical, offset=0, size=len(self.entries[canonical])
            )
        raise KeyError(f"Entry '{name}' not found in archive.")

    def read(self, name: str) -> bytes:
        """Reads and returns the byte payload for an archive entry.

        Args:
            name: Relative entry path inside the archive.

        Returns:
            bytes: The raw file content.

        Raises:
            KeyError: If the entry does not exist.
        """
        canonical = sanitize_path(name)
        if canonical not in self.entries:
            raise KeyError(f"Entry '{name}' not found in archive.")
        return self.entries[canonical]

    def open(self, name: str) -> io.BytesIO:
        """Returns a readable binary stream view over an archive entry's contents.

        Args:
            name: Relative entry path inside the archive.

        Returns:
            io.BytesIO: Binary stream positioned at byte 0.
        """
        return io.BytesIO(self.read(name))

    def extract(self, name: str, dest_dir: Path | str = ".") -> Path:
        """Safely extracts a single entry to disk.

        Args:
            name: Entry path inside the archive to extract.
            dest_dir: Target directory where the file will be saved.

        Returns:
            Path: The destination file path where content was written.
        """
        canonical = sanitize_path(name)
        data = self.read(canonical)
        target = safe_extract_path(Path(dest_dir), canonical)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return target

    def extractall(self, dest_dir: Path | str = ".") -> Path:
        """Safely extracts all archive entries to the destination directory.

        Args:
            dest_dir: Destination folder path.

        Returns:
            Path: The resolved destination path.
        """
        dest_path = Path(dest_dir)
        dest_path.mkdir(parents=True, exist_ok=True)
        for name in self.entries:
            self.extract(name, dest_path)
        return dest_path

    # --- Adding Entries ---

    def writestr(self, arcname: str, data: bytes | str) -> None:
        """Adds an in-memory entry to the archive.

        Args:
            arcname: The relative destination path inside the archive.
            data: Raw bytes or string payload (strings are UTF-8 encoded).
        """
        canonical = sanitize_path(arcname)
        payload = data.encode("utf-8") if isinstance(data, str) else bytes(data)
        self.entries[canonical] = payload

    def write(self, file_path: Path | str, arcname: str | None = None) -> None:
        """Reads a file from disk and adds it to the archive.

        Args:
            file_path: Path to the local file to add.
            arcname: Custom entry name inside the archive. Defaults to file_path.name.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: '{path}'")
        target_name = arcname if arcname is not None else path.name
        self.writestr(target_name, path.read_bytes())

    # --- Loading & Deserialization ---

    def load(self, source: Path | str | bytes | BinaryIO) -> None:
        """Parses and deserializes a .brarchive payload into this instance.

        Unpacks the binary layout:
        1. Reads 16-byte header: verifies magic 0x267052A0B125277D and version 1.
        2. Calculates Content Base = 16 + (count * 256).
        3. Parses each 256-byte descriptor record to extract:
           - Name length (uint8 at offset 0)
           - Name string (UTF-8 bytes 1..1+L)
           - Content Offset & Length (uint32 LE at offsets 248 and 252)
        4. Slices raw payload bytes from Content Base + Offset.

        Args:
            source: Archive file path, raw bytes buffer, or stream.

        Raises:
            BadArchiveError: If the archive is truncated, magic mismatches, or bounds fail.
            UnsupportedVersionError: If the version integer is not 1.
        """
        if isinstance(source, (str, Path)):
            path = Path(source)
            if not path.exists():
                raise FileNotFoundError(f"Archive file not found: '{path}'")
            raw = path.read_bytes()
        elif isinstance(source, (bytes, bytearray, memoryview)):
            raw = bytes(source)
        elif hasattr(source, "read"):
            raw = source.read()
        else:
            raise TypeError(f"Unsupported source type: {type(source)}")

        total_size = len(raw)
        if total_size < HEADER_SIZE:
            raise BadArchiveError(
                f"Data is too short for a header ({total_size} < {HEADER_SIZE} bytes)."
            )

        # 1. Unpack Header: Magic (u64 LE), Entry Count (u32 LE), Version (u32 LE)
        # Format "<QII": < = Little-Endian, Q = uint64 (8B), I = uint32 (4B), I = uint32 (4B)
        magic, count, version = struct.unpack_from("<QII", raw, 0)
        if magic != MAGIC:
            raise BadArchiveError(
                f"Invalid magic: {hex(magic)} (expected {hex(MAGIC)})."
            )
        if version != VERSION:
            raise UnsupportedVersionError(f"Unsupported archive version: {version}.")

        # 2. Content Base marks the start of raw file bytes after all descriptors
        content_base = HEADER_SIZE + count * DESCRIPTOR_SIZE
        if total_size < content_base:
            raise BadArchiveError(
                f"Archive truncated: requires {content_base} bytes for descriptors, but file is {total_size} bytes."
            )

        self.entries.clear()
        self._infos.clear()

        # 3. Parse Descriptors (256 bytes per entry)
        for i in range(count):
            desc_offset = HEADER_SIZE + i * DESCRIPTOR_SIZE
            name_len = raw[desc_offset]
            if name_len > MAX_NAME_LEN:
                raise InvalidEntryError(
                    f"Descriptor {i} specifies name length {name_len} > {MAX_NAME_LEN}."
                )

            name_bytes = raw[desc_offset + 1 : desc_offset + 1 + name_len]
            try:
                name = name_bytes.decode("utf-8")
            except UnicodeDecodeError as e:
                raise BadArchiveError(f"Descriptor {i} has invalid UTF-8 name.") from e

            canonical_name = sanitize_path(name)

            # Unpack Content Offset (uint32 LE) and Content Length (uint32 LE) at bytes 248..255
            offset, size = struct.unpack_from("<II", raw, desc_offset + 248)

            start = content_base + offset
            end = start + size
            if end > total_size:
                raise BadArchiveError(
                    f"Entry '{canonical_name}' offset out of bounds: requires byte {end}, file is {total_size} bytes."
                )

            # Extract entry slice and register metadata
            self.entries[canonical_name] = raw[start:end]
            self._infos.append(
                ArchiveInfo(name=canonical_name, offset=offset, size=size)
            )

    # --- Saving & Serialization ---

    def to_bytes(self) -> bytes:
        """Serializes this archive into binary .brarchive format in bytes.

        Serialization Workflow:
        1. Deterministically sort entry names for reproducible archive generation.
        2. Deduplication:
           - If deduplicate=True: compute SHA-256 for each payload. If the exact same
             payload has already been recorded, assign the existing Content Offset so
             both descriptors share the same content slice without writing it twice.
           - If deduplicate=False: append every entry payload sequentially.
        3. Pack 16-byte header: struct.pack("<QII", MAGIC, count, VERSION).
        4. Pack 256-byte descriptors: [length (1B), name (247B padded), offset (4B), size (4B)].
        5. Append the concatenated content section bytes.

        Returns:
            bytes: The complete serialized .brarchive binary file content.
        """
        count = len(self.entries)
        if count > 0xFFFFFFFF:
            raise BadArchiveError(f"Entry count {count} exceeds uint32 limit.")

        # Canonical alphabetical sort ensures bit-for-bit reproducible packaging
        sorted_names = sorted(self.entries.keys())

        descriptors: list[tuple[bytes, int, int]] = []
        unique_chunks: list[bytes] = []
        current_offset = 0

        if self.deduplicate:
            # Map SHA-256 digest -> Content Offset
            seen_hashes: dict[str, int] = {}
            for name in sorted_names:
                data = self.entries[name]
                digest = hashlib.sha256(data).hexdigest()

                if digest in seen_hashes:
                    # Reuse existing offset for duplicate payload
                    offset = seen_hashes[digest]
                else:
                    offset = current_offset
                    seen_hashes[digest] = offset
                    unique_chunks.append(data)
                    current_offset += len(data)

                descriptors.append((name.encode("utf-8"), offset, len(data)))
        else:
            for name in sorted_names:
                data = self.entries[name]
                offset = current_offset
                unique_chunks.append(data)
                current_offset += len(data)
                descriptors.append((name.encode("utf-8"), offset, len(data)))

        # Build binary archive buffer
        buf = bytearray()

        # Step 1: 16-Byte Header
        # < = Little-endian, Q = uint64 magic (8B), I = uint32 count (4B), I = uint32 version (4B)
        buf.extend(struct.pack("<QII", MAGIC, count, VERSION))

        # Step 2: 256-Byte Entry Descriptors
        for name_bytes, offset, size in descriptors:
            desc = bytearray(DESCRIPTOR_SIZE)
            desc[0] = len(name_bytes)
            desc[1 : 1 + len(name_bytes)] = name_bytes
            # Store offset and size at descriptor bytes 248..255 (format "<II")
            struct.pack_into("<II", desc, 248, offset, size)
            buf.extend(desc)

        # Step 3: Content Section (raw payload chunks)
        for chunk in unique_chunks:
            buf.extend(chunk)

        # Cache descriptors metadata
        self._infos = [
            ArchiveInfo(name=name_bytes.decode("utf-8"), offset=offset, size=size)
            for name_bytes, offset, size in descriptors
        ]

        return bytes(buf)

    def save(self, path: Path | str) -> Path:
        """Serializes and writes the archive to disk.

        Args:
            path: Destination file path.

        Returns:
            Path: The output file path.
        """
        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(self.to_bytes())
        return out_path

    # --- Class Convenience Methods ---

    @classmethod
    def pack(
        cls,
        source: Path | str,
        output: Path | str | None = None,
        *,
        deduplicate: bool = True,
        exclude: Iterable[str] = DEFAULT_EXCLUDES,
    ) -> Path:
        """Packs a folder or file directly into a .brarchive file.

        Args:
            source: Path to the directory or single file to archive.
            output: Optional custom output file path. Defaults to <source>.brarchive.
            deduplicate: Enable SHA-256 payload deduplication (default: True).
            exclude: Filename glob patterns to exclude (default: .git, Thumbs.db, etc.).

        Returns:
            Path: The path to the compiled .brarchive file.
        """
        src_path = Path(source)
        if not src_path.exists():
            raise FileNotFoundError(f"Source path does not exist: '{src_path}'")

        # Determine output file path
        if output is None:
            out_path = (
                src_path.with_suffix(".brarchive")
                if src_path.is_file()
                else src_path.parent / f"{src_path.name}.brarchive"
            )
        else:
            out_path = Path(output)
            if out_path.suffix != ".brarchive":
                out_path = out_path.with_suffix(".brarchive")

        exclude_list = tuple(exclude)
        archive = cls(deduplicate=deduplicate)

        if src_path.is_file():
            archive.write(src_path, arcname=src_path.name)
        else:
            # Walk directory and filter excluded files
            for item in sorted(src_path.rglob("*")):
                if not item.is_file():
                    continue

                rel_parts = item.relative_to(src_path).parts
                if any(
                    any(fnmatch.fnmatch(part, pat) for pat in exclude_list)
                    for part in rel_parts
                ):
                    continue

                rel_name = item.relative_to(src_path).as_posix()
                archive.write(item, arcname=rel_name)

        return archive.save(out_path)

    @classmethod
    def unpack(
        cls, archive_path: Path | str, output_dir: Path | str | None = None
    ) -> Path:
        """Unpacks a .brarchive file (or folder of .brarchive files) to disk.

        Args:
            archive_path: Path to the .brarchive file or folder of .brarchive files.
            output_dir: Optional extraction directory. Defaults to <archive_name> folder.

        Returns:
            Path: Destination extraction directory.
        """
        target_src = Path(archive_path)
        if not target_src.exists():
            raise FileNotFoundError(f"Archive path does not exist: '{target_src}'")

        if target_src.is_file():
            out_dir = (
                Path(output_dir) if output_dir else target_src.parent / target_src.stem
            )
            archive = cls(target_src)
            return archive.extractall(out_dir)
        else:
            # Recursively unpack all .brarchive files inside directory
            out_base = Path(output_dir) if output_dir else target_src
            archives = list(target_src.rglob("*.brarchive"))
            if not archives:
                raise FileNotFoundError(f"No .brarchive files found in '{target_src}'")
            for arc_file in archives:
                rel = arc_file.relative_to(target_src)
                dest = out_base / rel.with_suffix("")
                archive = cls(arc_file)
                archive.extractall(dest)
            return out_base

    @classmethod
    def from_bytes(cls, data: bytes | bytearray | memoryview) -> BrArchive:
        """Constructs a BrArchive instance directly from in-memory bytes.

        Args:
            data: Raw .brarchive bytes.

        Returns:
            BrArchive: Populated archive instance.
        """
        return cls(bytes(data))
